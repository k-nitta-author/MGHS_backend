from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'

# connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@localhost:3306/mghs"

# connection string for docker
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@host.docker.internal:3306/mghs"   

db = SQLAlchemy(app)

class User(db.Model):
    
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

    team_id=db.Column(db.Integer,db.ForeignKey("team.id"), nullable=True)
    
    phone_number=db.Column(db.String(50))

    
class Team(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))

class Task(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300), unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

class Activity(db.Model):
    id=db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(300))
    status = db.Column(db.String(20))

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))

class ActivitySubscription(db.Model):
    activity_id=db.Column(db.Integer, db.ForeignKey("activity.id"),  primary_key=True)
    intern_id=db.Column(db.Integer, db.ForeignKey("user.id"),  primary_key=True)
    
    reflection=db.Column(db.String(300))

    begin_date=db.Column(db.Date)
    end_date=db.Column(db.Date, nullable=True)

    is_complete=db.Column(db.Boolean)


if __name__ == "__main__":

    with app.app_context() as context:

        db.create_all()