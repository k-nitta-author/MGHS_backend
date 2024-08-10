from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy




class appointmentResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


        @app.route('/appointment', methods=['GET'])
        def get_all_appointments():

            appointments = self.model().query.all()
            output=[]

            appointment_data = []

            for appointment in appointments:
                appointment_data = {
                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,
                     "appointment_time":appointment.appointment_time,

                }

                output.append(appointment_data)


            return jsonify({"appointments": output})

        @app.route('/service/<id>', methods=['GET'])
        def get_one_appoinment(id):

            appointment = self.model().query.filter_by(id=id).first()

            if not appointment:
                return jsonify({'message': 'No appointment_data found'})



            appointment_data = {

                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,
                     "appointment_time":appointment.appointment_time,
            }

            return jsonify({'appointment': appointment_data})

        @app.route('/appointment', methods=['POST'])
        def create_appointment():

            data = request.get_json()


            appointment = self.model(

                    user_id=data['user_id'],
                    service_id=data['service_id'],
                    status=data['status'],
                    appointment_date=data['appointment_date'],
                    appointment_time=data['appointment_time']

                    )
            
            self.db.session.add(appointment)
            self.db.session.commit()

            return jsonify({'message': 'new appointment created'})

        @app.route('/appointment/<id>', methods=['DELETE'])
        def delete_appointment(id):

            appointment = self.model().query.filter_by(id=id).first()

            if not appointment:
                return jsonify({'message': 'No appointment found'})


            self.db.session.delete(appointment)
            self.db.session.commit()

            return jsonify({'message': 'appointment has been deleted'})