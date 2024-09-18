from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth

import uuid
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from os import environ

from user import UserResource
from activity import ActivityResource
from task import TaskResource
from team import TeamResource


from tables import app, db

from tables import User

auth = HTTPTokenAuth('Bearer')
basic_auth = HTTPBasicAuth()

user_resource = UserResource()
team_resource = TeamResource()
activity_resource = ActivityResource()
task_resource = TaskResource()

@app.route('/')
@basic_auth.login_required
def dashboard():
    return "Hello World"


# one is intended to get the token by logging in if this is possible
@auth.verify_token
def verify_token(token):

    tokens= {"token1":"213"}


    if token == "ted": return "user"

    return False


# currently untested
@basic_auth.verify_password
def verify_password(username, password):

    user = User.query.filter_by(username=username).first()


    if user and check_password_hash(user.password, password):
        return username
    
@basic_auth.get_user_roles
def get_user_roles(username):

    try:
        user = User.query.filter_by(username=username).first()
        return "admin" if user.admin else "user"
    except:
        return "user"

if __name__ == '__main__':

    # CREATE A COMMA SEPARATED LIST OF MGHS EMAILS WHICH SHOULD RECIEVE NOTIFICATIONS OF NEW JOB APPLICATIONS
    environ['JOB_APPLICANT_EMAIL_ADDRESS_LIST'] = "k.nitta.it@gmail.com"

    # CREATE A COMMA SEPARATED LIST OF MGHS EMAILS WHICH SHOULD RECIEVE NOTIFICATIONS OF INQUIRIES
    environ['INQUIRY_EMAIL_ADDRESS_LIST'] = "joshuapicato2016@gmail.com"

    # SET UP ENVIRONMENT VARIABLES FOR THE GMAIL ACCOUNT
    environ['OPTIFLOW_ACCOUNTNAME'] = "optiflow.mghs@gmail.com"
    environ['OPTIFLOW_PASSWORD'] = "mhzz opbh fpdf kxgh"

    app.run(debug=True, host='0.0.0.0')