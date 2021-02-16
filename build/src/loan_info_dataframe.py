#!/usr/bin/env python
# loan_info_dataframe - alternate datafame implementation
__version__ = '0.0.1'
__author__ = 'Forest Mars' #

import csv
from datetime import date, timedelta
from datetime import datetime as dt
from decimal import Decimal

import pandas as pd


def csv_to_dict(file) -> dict:
    """ Given a csv with an integer id as the first column, returns dictionary containing tuple of remaining columns. """
    loan_dict = {}
    reader = csv.reader(open(file))
    for row in reader:
        key = int(row[0])
        if key in loan_dict:
            pass
        loan_dict[key] = tuple(row[1:])

    return loan_dict


class DataFrameImplementation():
    """ Alternate implementation using DataFrame format more suited in machine learning pipeline. """

    def __init__(self) -> None:
        cols = ['loan_id', 'event_type', 'post_date', 'amt']  # features for payment history predictive model.
        self.loans = csv_to_dict('data/loans.csv')  # randomly generated sample data
        self.loan_events = pd.read_csv('data/loan_events.csv', names=cols, index_col=False)
        self.loan_events = self.normalize_payment_info(self.loan_events)

    def check_balance(self, loan_id: int, date_to_check: str) :
        loan_info = self.loans[loan_id]
        loan_start = dt.strptime(loan_info[0], "%Y-%m-%d").date()
        self.initial_amt = Decimal(loan_info[1])
        self.date_to_check = dt.strptime(date_to_check, "%Y-%m-%d").date()
        self.check_period = self.date_to_check - loan_start

    def normalize_payment_info(self, loan_events: pd.DataFrame) -> pd.DataFrame:
        """ Expects a dataframe. Converts tx amounts into accounting values. Could also use a transformer pipe for this. """
        loan_events.loc[loan_events['event_type'] == 'payment', 'amt'] = -loan_events['amt']

        return loan_events

    def get_carry_by_date(self, loan_id, date: dt) -> Decimal:
        """ Given a loan_id and a datetime.date, returns balance outstanding on that date. Uses numpy under the hood, ofc. """
        for day in range(1, self.check_period.days):
            pay_events = self.loan_events[self.loan_events['loan_id'] == int(loan_id)].sort_values('post_date')  # sort not really needed but still nice.
            period_events = pay_events[pay_events['post_date'] <= str(self.date_to_check)]
            period_total = period_events['amt'].sum()
            balance_carried = self.initial_amt - period_total

        return balance_carried
