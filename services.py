from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy




class servicesResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


        @app.route('/service', methods=['GET'])
        def get_all_services():

            services = self.model().query.all()
            output=[]

            notif_data = []

            for service in services:
                service_data = {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "availability": service.availability,
                "price":service.price
                }


                output.append(service_data)


            return jsonify({"services": output})

        @app.route('/service/<id>', methods=['GET'])
        def get_one_service(id):

            service = self.model().query.filter_by(id=id).first()

            if not service:
                return jsonify({'message': 'No service_data found'})



            service_data = {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "availability": service.availability,
                "price":service.price
            }

            return jsonify({'services': service_data})

        @app.route('/service', methods=['POST'])
        def create_service():

            data = request.get_json()


            service = self.model(

                    name=data['name'],
                    description=data['description'],
                    availability=data['availability'],
                    price=data['price']

                    )
            
            self.db.session.add(service)
            self.db.session.commit()

            return jsonify({'message': 'new service created'})

        @app.route('/service/<id>', methods=['DELETE'])
        def delete_service(id):

            service = self.model().query.filter_by(id=id).first()

            if not service:
                return jsonify({'message': 'No service found'})
    

            self.db.session.delete(service)
            self.db.session.commit()

            return jsonify({'message': 'service deleted'})