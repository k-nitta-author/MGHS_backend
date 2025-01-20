from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from werkzeug.security import check_password_hash
from flask import Flask, jsonify, request, make_response

from datetime import datetime, timedelta
from time import time

from os import environ

import jwt

from functools import wraps

from os import environ

app = Flask(__name__)
app.secret_key = 'secret_key'

# connection string
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('CONNECTION_STRING')

# set the secret key
# app.secret_key = environ.get('SECRET_KEY')


# connection string for docker
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@host.docker.internal:3306/mghs"   

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "app_user"
    
    id =db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50), unique=True)    
    
    surname=db.Column(db.String(50))
    givenname=db.Column(db.String(50))
    dob=db.Column(db.Date, nullable=False)
    email=db.Column(db.String(50))
    register_date=db.Column(db.Date)
    
    username=db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(110))

    is_admin=db.Column(db.Boolean)
    is_intern=db.Column(db.Boolean)

    must_reset_password=db.Column(db.Boolean)

    batch=db.Column(db.Integer)

    team_id=db.Column(db.Integer,db.ForeignKey("teams.id", ondelete='SET NULL'), nullable=True)
    
    phone_number=db.Column(db.String(50))

    activities = db.relationship("Activity", secondary="activity_subscriptions", back_populates="users")

    
class Team(db.Model):

    __tablename__ = "teams"

    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))

    # get the team with the most members
    def get_team_with_most_members(self):
        return db.session.query(User).filter_by(team_id=self.id).count()

    members = db.relationship('User', backref='teams', cascade="save-update, merge")
    tasks = db.relationship('Task', backref='teams', cascade="all, delete-orphan")
    


class Task(db.Model):

    __tablename__ = "tasks"

    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete='SET NULL'), nullable=True)

    # TODO: TEST THIS FUNCTION
    def count_activities(self):
        return self.activities.query.filter_by(task_id=self.id).count()

    activities = db.relationship('Activity', backref='tasks', cascade="all, delete, delete-orphan")

class Activity(db.Model):

    __tablename__ = "activities"

    id=db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))
    status = db.Column(db.String(20))
    rating = db.Column(db.Integer)

    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))

    users = db.relationship("User", secondary="activity_subscriptions", back_populates="activities")
    subscriptions = db.relationship("ActivitySubscription", backref="activities", cascade="all, delete, delete-orphan")

class ActivitySubscription(db.Model):

    __tablename__ = "activity_subscriptions"

    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"), primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), primary_key=True)
    
    reflection = db.Column(db.String(300))

    begin_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)

    is_complete = db.Column(db.Boolean)

    activity = db.relationship("Activity", back_populates="subscriptions")
    intern = db.relationship("User", back_populates="subscriptions")

# authenticate the user
# requires basic authentication with username and password
# returns a token that is valid for 10 hours
# the token is used to authenticate the user for other requests
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Missing username or password"}), 401

    username = auth.username
    password = auth.password

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    token = jwt.encode({'user': user.username, 'exp': datetime.now() + timedelta(hours=10)}, app.secret_key)
    return jsonify(
        {
            "login_token": token,
            "username": user.username,
            "public_id": user.public_id,
            "is_admin": user.is_admin
        }
    )

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):


        try:
            token = request.authorization.token

        except AttributeError:
            return jsonify({"message": "token is missing!"}), 403

        if not token:
            return jsonify({"message": "token is missing!"}), 403
        
        try:
            data = jwt.decode(token, app.secret_key, algorithms="HS256")

            print({"message": "token has expired!", "exp": data['exp'], "time":time()})

        except:
            return jsonify({"message": "Token is invlalid"}), 403
        
        return f(*args,**kwargs)
    
    return decorated

def auth_role(role):
    
    def wrapper(f):
        @wraps(f)
        def decorated(*args,**kwargs):

            auth = request.authorization

            token = request.authorization.token

            data = jwt.decode(token, app.secret_key, algorithms="HS256")
            
            u: User = User.query.filter_by(username=data['user']).first()

            allowed = False

            match role:
            
                case "admin": 
                    allowed=u.is_admin
                case "intern":
                    allowed=u.is_intern

                case _:
                    pass

            if not allowed: return jsonify({"message": "insufficient access credentials"})

            return f(*args,**kwargs)
    
        return decorated
    
    return wrapper

if __name__ == "__main__":

    with app.app_context() as context:

        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

        try:
            Team.__table__.create(bind=engine)
            User.__table__.create(bind=engine)
            Task.__table__.create(bind=engine)
            Activity.__table__.create(bind=engine)
            ActivitySubscription.__table__.create(bind=engine)

        # currently checks if there was a duplicate table error
        except ProgrammingError as e:

            print(e._message)
            

        db.session.commit()