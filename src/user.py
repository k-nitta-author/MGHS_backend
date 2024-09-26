from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from tables import db, app, User as model

import uuid
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from tables import login, token_required, auth_role


class UserResource:

    def __init__(self) -> None:
        
        self.register_routes()

    def create_public_id(self) -> str:

        return str(uuid.uuid4())

    def register_routes(self) -> None:

        
        @app.route('/user', methods=['GET'])
        def get_all_users():

            users = model().query.all()
            output=[]

            user_data = []

            for user in users:

                user : model = user

                input = {

                    "id":user.id,
                    "batch": user.batch,
                    "givenname": user.givenname,
                    "dob":user.dob,
                    "is_admin": user.is_admin,
                    "surname": user.surname,
                    "email": user.email,
                    "is_intern":user.is_intern,

                    "password": user.password,
                    "username": user.username,

                    "phone_number":user.phone_number,
                    "public_id":user.public_id,
                    "register_date":user.register_date,
                    "team_id":user.team_id,
                    

                }


                output.append(input)


            return jsonify({"user": output})
        
        
        @app.route('/user/<id>', methods=['GET'])
        @auth_role("admin")
        def get_one_user(id):

            user = model().query.filter_by(public_id=id).first()

            if not user:
                return jsonify({'message': 'No user found'})



            user_data = {

                    "id":user.id,
                    "batch": user.batch,
                    "givenname": user.givenname,
                    "dob":user.dob,
                    "is_admin": user.is_admin,
                    "surname": user.surname,
                    "email": user.email,
                    "is_intern":user.is_intern,

                    "password": user.password,
                    "username": user.username,

                    "phone_number":user.phone_number,
                    "public_id":user.public_id,
                    "register_date":user.register_date,
                    "team_id":user.team_id,

            }

            return jsonify({'user': user_data})

        @app.route('/user', methods=['POST'])
        def create_user():

            data = request.get_json()


            user = model()

            u_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

            user.dob = data["dob"]
            user.batch = data["batch"]
            user.givenname = data["givenname"]
            user.surname = data["surname"]
            user.is_admin = data["is_admin"]
            user.is_intern = data["is_intern"]
            user.password = u_password
            user.username = data["username"]

            user.phone_number = data["phone_number"]
            user.public_id = self.create_public_id()


            user.register_date = datetime.now()
            user.team_id = data["team_id"]
            
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'new user created'})

        @app.route('/user/<id>', methods=['DELETE'])
        def delete_user(id):

            user = model().query.filter_by(public_id=id).first()

            if not user:
                return jsonify({'message': 'No user found'})
    

            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'user has been deleted'})
        

        @app.route('/user/<id>', methods=['PUT'])
        def update_user(id):
            data = request.get_json()


            user = model().query.filter_by(public_id=id).first()

            user.dob = data["dob"]
            user.batch = data["batch"]
            user.givenname = data["givenname"]
            user.surname = data["surname"]
            user.is_admin = data["is_admin"]
            user.is_intern = data["is_intern"]
            user.password = data["password"]

            user.phone_number = data["phone_number"]

            user.register_date = data["register_date"]
            user.team_id = data["team_id"]
            
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'new user created'})