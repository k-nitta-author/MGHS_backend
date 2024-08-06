from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flask_httpauth import HTTPBasicAuth

import uuid

from notifications import notificationsResource
from services import servicesResource
from job import JobResource
from appointment import appointmentResource

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:koolele@localhost:3306/mghs"   

auth = HTTPBasicAuth()

db = SQLAlchemy(app)

class User(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50), unique=True)
    name=db.Column(db.String(50))
    username=db.Column(db.String(50))
    password=db.Column(db.String(110))
    admin=db.Column(db.Boolean)
    phone_number=db.Column(db.String(50))

class Service(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    description=db.Column(db.String(50))
    availability=db.Column(db.String(50))
    price=db.Column(db.DECIMAL())

class Appointment(db.Model):
    appointment_id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    service_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    status=db.Column(db.String(50))

class Job(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    jobTitle=db.Column(db.String(50))
    jobRequest=db.Column(db.String(100))
    jobRequirements=db.Column(db.String(100))
    

class Notification(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    message=db.Column(db.String(50))
    isReady=db.Column(db.Integer)

resource_notif = notificationsResource(app, db, Notification)
resource_service = servicesResource(app, db, Service)
resource_job = JobResource(app, db, Job)
resource_appoinment = appointmentResource(app, db, Appointment)

@app.route('/')
@auth.login_required
def dashboard():
    return "Hello World"

@app.route('/user', methods=['GET'])
def get_all_users():

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

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'new user created'})

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No ser found'})
    

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'user has been deleted'})

@app.route('/user', methods=['PUT'])
def promote_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No ser found'})
    

    db.session.commit()

    return jsonify({'message': 'user has been updated'})


@app.route('/login')
@auth.verify_password
def verify_password(username, password):

    user = User.query.filter(User.username == username).first()

    if user and check_password_hash(user.password , password):

        return user.username   
    
if __name__ == '__main__':
    app.run(debug=True)