from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy




class notificationsResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


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
                "message": notif.id,
                "isReady": notif.id,
            }

            return jsonify({'user': notif_data})

        @app.route('/notification', methods=['POST'])
        def create_notif():

            data = request.get_json()


            new_user = self.model(

                    message=data['message'],
                    isReady=data['isReady']

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