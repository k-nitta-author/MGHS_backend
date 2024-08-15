from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


class UserResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


        @app.route('/job', methods=['GET'])
        def get_all_users():

            users = self.model().query.all()
            output=[]

            user_data = []

            for user in users:
                user_data = {

                }


                output.append(user_data)


            return jsonify({"user": output})

        @app.route('/user/<id>', methods=['GET'])
        def get_one_user(id):

            user = self.model().query.filter_by(id=id).first()

            if not user:
                return jsonify({'message': 'No user found'})



            user_data = {

            }

            return jsonify({'user': user_data})

        @app.route('/user', methods=['POST'])
        def create_user():

            data = request.get_json()


            user = self.model(


                    )
            
            self.db.session.add(user)
            self.db.session.commit()

            return jsonify({'message': 'new user created'})

        @app.route('/user/<id>', methods=['DELETE'])
        def delete_user(id):

            user = self.model().query.filter_by(id=id).first()

            if not user:
                return jsonify({'message': 'No user found'})
    

            self.db.session.delete(user)
            self.db.session.commit()

            return jsonify({'message': 'user has been deleted'})