#!/usr/bin/env python
# app.py - Expose API for loan paymnt information.
__version__ = '0.0.1'
__author__ = 'Forest Mars' #

import os
from datetime import datetime as dt
from datetime import timedelta
import logging

from flask import Flask, Response, jsonify, redirect, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restx import Api, Resource  # See README.md#known-issues
from redis import Redis
#from rq import Queue
from waitress import serve

# If compiled C class is n/a, fall back on source file.
try:
    from lib.ext.loan_info import LoanInfoService
except ImportError:
    from build.src.loan_info import LoanInfoService


SECRET = os.environ['SECRET']


logger = logging.getLogger(__name__)

wsgi_app = Flask(__name__)
wsgi_app.config['JWT_SECRET_KEY'] = os.environ['API_KEY']
wsgi_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.environ['ACCESS_TOKEN_EXPIRES']
app = Api(app = wsgi_app)
jwt = JWTManager(wsgi_app)
app.namespaces.clear()  # api.namespaces.pop(0) or api.namespaces = [] also works here.
loan_info = app.namespace('api/v1/', description='Loan Info Service, v. 0.1')


# Requesting access token can be included in API, or required prior to API access.
@wsgi_app.route('/token', methods=['POST'])
def APIAccessToken():  # Endpoint to generate JWT access token required for API access.
    user = request.json.get('user', None)
    pw = request.json.get('pw', None)
    if password != SECRET:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=user)

    return jsonify(access_token=access_token)

"""
class AccessToken():  # API endpoint to generate JWT access tokens.

    def get():
        user = request.json.get('user', None)
        pw = request.json.get('pw', None)
        if password != SECRET:
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=user)

        return jsonify(access_token=access_token)
"""

@jwt_required
@app.route('/status')
class LoanHome(Resource):
    """ Mainly provides health check for testing endpoint. """
    def get(self):
        return {
            "status": "Loan Info µ-Service is running."
    }

@app.route('/api/v1')
class LoanHome(Resource):
    """ Redirect API requests. """
    def get(self):
        return redirect('/')

@app.route('/api')
class LoanHome(Resource):
    """ Redirect API requests. """
    def get(self):
        return redirect('/')


# @jwt_required  -- For our demo, we don't require secure access.
# @loan_info.route("/loan/<int:id>/<date>", methods = ['GET'])
@loan_info.route("/loan/<int:id>/<date>", methods = ['GET'])
class LoanInfo(Resource):

    def get(self, id, date):
        """ Expects a loan_id and a properly formatted date string. Makes some effort to match a poorly formatted date string. """
        if not isinstance(id, int):
            resp = "Sorry, that is not a valid loan id."
            return Response(resp, mimetype='text/xml')
        elif not isinstance(date, str):  # :-|
            resp = "Sorry, that doesn't seem to be a valid date."
            return Response(resp, mimetype='text/xml')
        else:
            valid_date = self.parse_date(date)

        if valid_date is None:
            resp = "Sorry, that doesn't seem to be a valid date."
            return Response(resp, mimetype='text/xml')
        else:
            resp = self.handle_request(id, date)
            return resp

    def parse_date(self, req_date):
        try:
            chk_date = dt.strptime(req_date, "%Y-%m-%d")
            if isinstance(chk_date, dt):
                return req_date  # :-|
            else:
                return None
        except Exception as e:
            print("Probably a malformed date - ", e)

    def handle_request(self, id: int, date: str) -> float:
        loan_info = LoanInfoService()
        try:
            get_balance = str(loan_info.get_balance_due(id, date))
            return get_balance
        except Exception as e:
            logger.error(e)
            return "Service temporarily unavailable."



if __name__ == '__main__':
        serve(wsgi_app, host='0.0.0.0', port=5555, url_scheme='https') # waitress
