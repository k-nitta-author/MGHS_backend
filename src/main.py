from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth

import uuid

from notifications import notificationsResource
from services import servicesResource
from job import JobResource
from appointment import appointmentResource

from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

# connection string
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@localhost:3306/mghs"

# connection string for docker
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@host.docker.internal:3306/mghs"   


auth = HTTPTokenAuth('Bearer')
basic_auth = HTTPBasicAuth()

db = SQLAlchemy(app)

class User(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50), unique=True)
    name=db.Column(db.String(50))
    username=db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(110))
    admin=db.Column(db.Boolean)
    phone_number=db.Column(db.String(50))

class Service(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True)
    description=db.Column(db.String(200))
    availability=db.Column(db.Boolean)
    price = db.Column(db.DECIMAL(10, 2))

class Appointment(db.Model):
    appointment_id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    service_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    status=db.Column(db.String(50), nullable=False)
    appointment_date=db.Column(db.Date, nullable=False)
    appointment_time=db.Column(db.Time, nullable=False)

class Job(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    jobTitle=db.Column(db.String(50), unique=True)
    jobRequirements=db.Column(db.String(100))
    available=db.Column(db.Boolean)
    

class Notification(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    message=db.Column(db.String(50))
    isReady=db.Column(db.Integer)
    timeCreated=db.Column(db.DateTime(timezone=True), server_default=db.func.now())

resource_notif = notificationsResource(app, db, Notification)
resource_service = servicesResource(app, db, Service)
resource_job = JobResource(app, db, Job)
resource_appoinment = appointmentResource(app, db, Appointment)

@app.route('/')
@basic_auth.login_required
def dashboard():
    return "Hello World"

@app.route('/user', methods=['GET'])
@basic_auth.login_required(role="admin")
def get_all_users():

    print(basic_auth.current_user)

    users = User.query.all()
    output=[]

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['phone_number']=user.phone_number
        user_data['public_id'] = user.public_id

        output.append(user_data)


    return jsonify({"users": output})

@app.route('/user/<public_id>', methods=['GET'])
@basic_auth.login_required
def get_one_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No ser found'})

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['phone_number']=user.phone_number
    user_data['public_id'] = user.public_id

    return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(
                    public_id=str(uuid.uuid4()),
                    phone_number=data['phone_number'],
                    name=data['name'],
                    password=hashed_password,
                    admin=False,
                    username=data['username']
                    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'new user created'})

    except:
        return jsonify({"message": "missing/incorrect data"})
    
@app.route('/user/<public_id>', methods=['DELETE'])
@basic_auth.login_required(role="admin")
def delete_user(public_id):
    notif = User.query.filter_by(public_id=public_id).first()

    if not notif:
        return jsonify({'message': 'No user found'})
    

    db.session.delete(notif)
    db.session.commit()

    return jsonify({'message': 'user has been deleted'})

@app.route('/user/<public_id>/promote', methods=['PUT'])
@basic_auth.login_required(role="admin")
def promote_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No ser found'})

    user.admin=True    

    db.session.commit()

    return jsonify({'message': 'user has been promoted'})

@app.route('/user/<public_id>/demote', methods=['PUT'])
@basic_auth.login_required(role="admin")
def demote_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No ser found'})

    user.admin=False    

    db.session.commit()

    return jsonify({'message': 'user has been demoted'})

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


print("asdas")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')