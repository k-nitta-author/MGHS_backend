from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy


from werkzeug.security import check_password_hash
from flask import Flask, jsonify, request, make_response

from datetime import datetime, timedelta
from time import time

import jwt


from functools import wraps


app = Flask(__name__)
app.secret_key = 'secret_key'

# connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@localhost:3306/mghs"

# connection string for docker
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@host.docker.internal:3306/mghs"   

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "users"
    
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

    batch=db.Column(db.Integer)

    team_id=db.Column(db.Integer,db.ForeignKey("teams.id", ondelete='SET NULL'), nullable=True)
    
    phone_number=db.Column(db.String(50))

    activities = db.relationship("Activity", secondary="activity_subscriptions", back_populates="users")

    
class Team(db.Model):

    __tablename__ = "teams"

    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))

    members = db.relationship('User', backref='teams', cascade="all")
    tasks = db.relationship('Task', backref='teams', cascade="all")


class Task(db.Model):

    __tablename__ = "tasks"

    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete='SET NULL'), nullable=True)

    activities = db.relationship('Activity', backref='tasks', cascade="all, delete, delete-orphan")

class Activity(db.Model):

    __tablename__ = "activities"

    id=db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))
    status = db.Column(db.String(20))

    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))

    users = db.relationship("User", secondary="activity_subscriptions", back_populates="activities")

class ActivitySubscription(db.Model):

    __tablename__ = "activity_subscriptions"

    activity_id=db.Column(db.Integer, db.ForeignKey("activities.id"),  primary_key=True)
    intern_id=db.Column(db.Integer, db.ForeignKey("users.id"),  primary_key=True)
    
    reflection=db.Column(db.String(300))

    begin_date=db.Column(db.Date)
    end_date=db.Column(db.Date, nullable=True)

    is_complete=db.Column(db.Boolean)

@app.route('/login')
def login():
    auth = request.authorization.parameters

    username  = auth.get('username', "")

    password  = auth.get('password', "")

    user: User = User.query.filter_by(username=username).first()


    if not user or not password:
        return jsonify({"message": "no password or username or user"})

    if user and check_password_hash(user.password, password):

        token = jwt.encode({'user': user.username, 'exp': datetime.now() + timedelta(seconds=10)}, app.secret_key)

        return jsonify(
            {
                "login_token": token,
                "username": user.username
                }
            )

    return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

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

        db.create_all()