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
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is Missing'})

        try:
            data = jwt.decode(token, app.secret_key)
            current_user = User.query.filter_by(public_id=data['public_id']).first()

        except:
            return jsonify({'message': 'Token is Invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm=Login required'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm=Login required'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'expiration': datetime.datetime.now() + datetime.timedelta(minutes=30),
            },
             app.secret_key
        )

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm=Login required'})
if __name__ == '__main__':
    app.run(debug=True)