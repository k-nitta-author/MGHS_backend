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

        # gets a single service based on the id
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


        # creates a new unique service
        @app.route('/service', methods=['POST'])
        def create_service():

            data = request.get_json()


            service = self.model(

                    name=data['name'],
                    description=data['description'],
                    availability=data['availability'],
                    price=data['price']

                    )
            try:
                self.db.session.add(service)
                self.db.session.commit()

                return jsonify({'message': 'new service created'})
            
            except:
                return jsonify({'message': 'incorrect-wrong or missing data'})

        # deletes the service
        @app.route('/service/<id>', methods=['DELETE'])
        def delete_service(id):

            service = self.model().query.filter_by(id=id).first()

            if not service:
                return jsonify({'message': 'No service found'})
    

            self.db.session.delete(service)
            self.db.session.commit()

            return jsonify({'message': 'service deleted'})
        

        # used to set service availability
        @app.route('/service/<id>/provide', methods=['PUT'])
        def provide_service(id):

            service = self.model().query.filter_by(id=id).first()

            if not service:
                return jsonify({'message': 'No service found'})
            
            service.available = True
    
            self.db.session.commit()

            return jsonify({'message': 'service is now available'})
        
        # used to remove service availability
        @app.route('/service/<id>/deprive', methods=['PUT'])
        def deprive_service(id):

            service = self.model().query.filter_by(id=id).first()

            if not service:
                return jsonify({'message': 'No service found'})
            
            service.available = False
    
            self.db.session.commit()

            return jsonify({'message': 'service is now unavailable'})
        

        # used to change multiple values in a service.
        @app.route('/service/<id>/deprive', methods=['PUT'])
        def alter_data_service(id):

            data = request.get_json()

            service = self.model().query.filter_by(id=id).first()

            if not service:
                return jsonify({'message': 'No service found'})


            service.name=data['name'],
            service.description=data['description'],
            service.availability=data['availability'],
            service.price=data['price']
    
            self.db.session.commit()

            return jsonify({'message': 'service is now unavailable'})
        
