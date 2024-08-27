from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from calendar import month_abbr

from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL
import ssl
from os import environ

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


            for appointment in appointments:
                appointment_data = {
                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,

                }

                output.append(appointment_data)


            return jsonify({"appointments": output})

        @app.route('/appointment/<id>', methods=['GET'])
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
            }

            return jsonify({'appointment': appointment_data})
        
        @app.route('/appointment/month/<month>', methods=['GET'])
        def get_by_month_appointment(month: int):

            month_idx = int(month)

            if month_idx > 12 or month_idx < 1: return jsonify({"message": "invalid month index"})

            appointments = self.model().query.filter(db.extract('month', self.model.appointment_date)==month_idx).all()

            current_abbreviation = month_abbr[month_idx]

            output=[]

            for appointment in appointments:
                appointment_data = {
                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,

                }

                output.append(appointment_data)

            return jsonify({"message": output})
        

        @app.route('/appointment/user/<user_id>', methods=['GET'])
        def get_by_user_appointment(user_id: int):


            appointments = self.model().query.filter_by(user_id=user_id)

            output=[]

            for appointment in appointments:
                appointment_data = {
                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,

                }

                output.append(appointment_data)

            return jsonify({"message": output})
        
        """
            STATUS SHOULD BE ONLY BETWEEN PENDING, IN_REVIEW, APPROVED, AND REJECTED
        
        """
        @app.route('/appointment/status/<status>', methods=['GET'])
        def get_by_status_appointment(status: str):


            appointments = self.model().query.filter_by(status=status)

            output=[]

            for appointment in appointments:
                appointment_data = {
                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,

                }

                output.append(appointment_data)

            return jsonify({"message": output})
        
        @app.route('/appointment/service/<service_id>', methods=['GET'])
        def get_by_service_appointment(service_id: int):


            appointments = self.model().query.filter_by(service_id=service_id)

            output=[]

            for appointment in appointments:
                appointment_data = {
                     "id":appointment.appointment_id,
                     "user_id":appointment.user_id,
                     "service_id": appointment.service_id,
                     "status":appointment.status,
                     "appointment_date":appointment.appointment_date,

                }

                output.append(appointment_data)

            return jsonify({"message": output})

        @app.route('/appointment', methods=['POST'])
        def create_appointment():

            data = request.get_json()


            appointment = self.model(

                    user_id=data['user_id'],
                    service_id=data['service_id'],
                    status='PENDING',
                    appointment_date=None,

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