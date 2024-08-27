from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

class notificationsResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object, user_model: object) -> None:
        
        self.register_routes(app, db, user_model)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy, user: object) -> None:


        @app.route('/notification', methods=['GET'])
        def get_all():

            notifs = self.model().query.all()
            output=[]

            notif_data = []

            for notif in notifs:
                notif_data = {
                "id": notif.id,
                "message": notif.message,
                "isReady": notif.isReady,
                "timeCreated":notif.timeCreated

                }

                output.append(notif_data)


            return jsonify({"notifs": output})

        @app.route('/notification/<id>', methods=['GET'])
        def get_one_notif(id):

            notif = self.model().query.filter_by(id=id).first()

            if not notif:
                return jsonify({'message': 'No ser found'})



            notif_data = {
                "id": notif.id,
                "message": notif.message,
                "isReady": notif.isReady,
                "user":notif.user,
                "timeCreated":notif.timeCreated
            }

            return jsonify({'user': notif_data})
        
        #TODO: GET NOTIFICATION BY USER ID
        @app.route('/notification/user/<id>', methods=['GET'])
        def get_notification_by_user(id):
            notifs = self.model().query.filter_by(user=id)

            print(notifs)

            if not notifs:
                return jsonify({'message': 'No ser found'})


            user_notifs = []

            for notif in notifs:
                notif_data = {
                    "id": notif.id,
                    "message": notif.message,
                    "isReady": notif.isReady,
                    "user":notif.user,
                    "timeCreated":notif.timeCreated
                }

                user_notifs.append(notif_data)

            return jsonify({'user': user_notifs})


        @app.route('/notification', methods=['POST'])
        def create_notif():

            data = request.get_json()


            new_user = self.model(

                    message=data['message'],
                    isReady=data['isReady'],
                    user=data['user'],
                    timeCreated=data['timeCreated']

                    )
            
            self.db.session.add(new_user)
            self.db.session.commit()

            return jsonify({'message': 'new user created'})

        @app.route('/notification/<id>', methods=['DELETE'])
        def delete_notif(id):

            notif = self.model().query.filter_by(id=id).first()

            if not notif:
                return jsonify({'message': 'No ser found'})
    

            self.db.session.delete(notif)
            self.db.session.commit()

            return jsonify({'message': 'notif has been deleted'})