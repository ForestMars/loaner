#!/usr/bin/env python
# run - non-compiiled version of loan_info demo. Requires running Postgres backend.
__version__ = '0.0.1'
__author__ = 'Forest Mars' #

from datetime import date, timedelta
from datetime import datetime as dt
from decimal import Decimal
import logging
import sys

import numpy as np
import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine, asc, desc
from sqlalchemy import Column, and_, Date, Enum, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text  # SQLalchemy 1.4.0b2 Beta
from protobuf_serialization import serialize_to_protobuf
from protobuf_serialization.serialization import ProtobufDictSerializer

from sqlalchemy.orm import mapper, relationship

from config.postgres import *
from config.redis import red


logger = logging.getLogger("Um")

try:
    engine = create_engine(SQL_URL)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
except Exception as e:
    sys.exit("Can't connect to database, exiting.")


class Loans(Base):
    """ Loan model """
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    initial_amt = Column(Numeric)


class LoanEvents(Base):
    """ Loan events model """
    __tablename__ = 'loan_events'
    event_types = ('fee', 'interest', 'payment')
    event_type_enum = Enum(*event_types, name="event_type")
    tx_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, primary_key=False, autoincrement=False, unique=False)
    event_type = Column(event_type_enum)
    post_date = Column(Date)
    amt = Column(Numeric)


class DBConnect():
    """ Connection class for handling SQL database queries. """
    def __init__(self):
        session = Session()
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        Base.query = db_session.query_property()

    def fetch(self, model: str, **kwargs):
        """ a basic sql fetcher that does not implement joins. """
        result = eval(model).query.filter_by(**kwargs)

        return result

    def fetch_first(self, model: str, **kwargs):
        """ sql fetcher for fifo queries. """
        result = eval(model).query.filter_by(**kwargs).first()

        return result

    def fetch_one(self, model: str, **kwargs):
        """ sql fetcher for singular queries. """
        result = eval(model).query.filter_by(**kwargs).one()

        return result

    def generator(self, model: str, **kwargs):
        """ generator for iterative sql querying. """
        result = eval(model).query.filter_by(**kwargs)

        for row in result:
            yield row


class LoanInfoService():
    """ Class to process requests for loan balance due by date. """

    def __init__(self) -> None:
        self.db = DBConnect()

    def schema_stream(self):
        """" Future method for decoupling db schema from event stream """
        pass

    def get_balance_due(self, id, date_to_check):
        bal_due = self.get_balance_by_date(id, date_to_check)
        resp = "\nAs of {0}, loan #{1} owed ${2}0\n".format(date_to_check, id, bal_due)

        return resp

    def get_balance_by_date(self, loan_id: int, date_to_check: date) -> Decimal:
        """ Check is result is cached, if not get result and set cache. """
        try:
             balance_carried = red.get('loan-' + str(loan_id) + ':' + date_to_check)  # Try redis cache for date_to_check
             if balance_carried is not None:
                 return balance_carried
        except Exception as e:
            pass  # cache miss, EAFP

        loan_info = self.get_loan_info(loan_id)
        loan_activity = self.get_loan_activity(loan_info)
        balance_carried = self.process_loan_activity(loan_info, loan_activity, date_to_check)
        red.set('loan-' + str(loan_id) + ':' + date_to_check, float(balance_carried))  # Cache final result in Redis

        return balance_carried

    def get_loan_info(self, loan_id: int) -> sqlalchemy.orm.query.Query:
        """ Fetches loan origin date and initial amount for a given loan. """
        response = self.db.fetch_one('Loans', loan_id=loan_id)
        loan_info = {'loan_id': loan_id, 'loan_origin': response.start_date, 'loan_amount': response.initial_amt}

        return loan_info

    def get_loan_activity(self, loan_info: dict)-> sqlalchemy.orm.query.Query:
        """ Fetches loan activity for a given loan.

        Args:
            loan_info: dict from which we just need the loan_id key.

        Returns:
            unserialized sqlalchemy db object.
        """
        try:
            current = dt.today().strftime("%Y-%m-%d")
            loan_activity = red.get('loan-' + loan_info['loan_id'] + '-activity:' + current)  # Try redis cache for activity to date
            if loan_activity is not None:
                return loan_activity
        except Exception as e:
            pass  # cache miss, EAFP

        loan_activity = self.db.fetch('LoanEvents', loan_id=loan_info['loan_id'])
        # loan_activity_cached = serialize_to_protobuf(loan_activity, ProtobufDictSerializer)  # @FIXME: DESCRIPTOR missing from proto_cls
        # red.set(str('loan-' + loan_info['loan_id']) + '-activity:' + current, loan_activity_cached)

        return loan_activity

    # A better solution (for permutation) might be to add a signed_amt column to LoanEvents.
    def process_loan_activity(self, loan_info: dict, loan_activity: LoanEvents, date_to_check: str):
        """ Given a LoanEvents object (of all history for a given loan id), returns only the dates needed to fulfill the lookup request. """
        period_activity = []
        period = lambda a: a <= date_to_check
        permutate = lambda a, b : -Decimal(a) if (b == 'payment') else Decimal(a)
        for loan in loan_activity:
            period_activity.append((
                loan.event_type,
                loan.post_date,
                permutate(loan.amt, loan.event_type),
                ))
        period_activity = tuple(period_activity)
        date_to_check_ = dt.strptime(date_to_check, "%Y-%m-%d").date()
        period_activity = tuple(filter(lambda x: x[1] <= date_to_check_, period_activity))
        transactions = np.sum(np.array(period_activity)[:,2])
        balance_carried = Decimal(loan_info['loan_amount']) + transactions

        return balance_carried




if __name__ == "__main__":

    # Example lookup
    print("\nSelect loan and date or ENTER for default example.")
    req_id = input("Which loan to look up? ") or 1
    req_date = input("Which date to check? (Y-m-d) ") or '2020-10-31'
    loan = LoanInfoService()
    result = loan.get_balance_by_date(req_id, req_date)
    print("\nAs of {0}, loan #{1} owed ${2}0\n".format(req_date, req_id, result))
