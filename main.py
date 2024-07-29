from flask import Flask, jsonify, request, make_response, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy

import jwt
import datetime

from functools import wraps

import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)
if __name__ == '__main__':
    app.run(debug=True)