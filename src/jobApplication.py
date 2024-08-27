from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL
import ssl
from os import environ

class JobApplicationResource:

    def __init__(self, app: Flask, db: SQLAlchemy, model: object, user_model: object, job_model: object) -> None:
        
        self.register_routes(app, db)
        self.model = model
        self.db = db
        self.user_model = user_model
        self.job_model = job_model

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:


        @app.route('/job_application', methods=['GET'])
        def get_all_job_application():

            job_applications = self.model().query.all()
            output=[]

            application_data = []

            for job_application in job_applications:
                job_application_data = {

                "user_id":job_application.user_id,
                "job_id":job_application.job_id,
                "interview_date":job_application.interview_date,
                "application_date":job_application.application_date,
                "application_source":job_application.application_source,
                "status": job_application.status
                }


                output.append(job_application_data)


            return jsonify({"job_applications": output})
        

        @app.route('/job_application/<user_id>', methods=['GET'])
        def get_by_user_job_application(user_id):

            job_applications = self.model().query.filter_by(user_id=user_id).all()

            if not job_applications:
                return jsonify({'message': 'No job_application found'})
            
            output=[]
            
            for job_application in job_applications: 

                job_application_data = {
                    "user_id":job_application.user_id,
                    "job_id":job_application.job_id,
                    "interview_date":job_application.interview_date,
                    "application_date":job_application.application_date,
                    "application_source":job_application.application_source,
                    "status":job_application.status

                }

                output.append(job_application_data)

            return jsonify({'job applications': output})
        
        @app.route('/job_application/job/<job_id>', methods=['GET'])
        def get_by_job_job_application(job_id):

            job_applications = self.model().query.filter_by(job_id=job_id).all()

            if not job_applications:
                return jsonify({'message': 'No job_application found'})
            
            output=[]
            
            for job_application in job_applications: 

                job_application_data = {
                    "user_id":job_application.user_id,
                    "job_id":job_application.job_id,
                    "interview_date":job_application.interview_date,
                    "application_date":job_application.application_date,
                    "application_source":job_application.application_source,
                    "status":job_application.status
                }

                output.append(job_application_data)

            return jsonify({'job applications': output})
        
        @app.route('/job_application/status/<status>', methods=['GET'])
        def get_by_status_job_application(status):

            job_applications = self.model().query.filter_by(status=status).all()

            if not job_applications:
                return jsonify({'message': 'No job_application found'})
            
            output=[]
            
            for job_application in job_applications: 

                job_application_data = {
                    "user_id":job_application.user_id,
                    "job_id":job_application.job_id,
                    "interview_date":job_application.interview_date,
                    "application_date":job_application.application_date,
                    "application_source":job_application.application_source,
                    "status":job_application.status
                }

                output.append(job_application_data)

            return jsonify({'job applications': output})

        @app.route('/job_application/<user_id>/<job_id>', methods=['GET'])
        def get_one_job_application(user_id, job_id):

            job_application = self.model().query.get((user_id,job_id))

            if not job_application:
                return jsonify({'message': 'No job_application found'})

            job_application_data = {
                "user_id":job_application.user_id,
                "job_id":job_application.job_id,
                "interview_date":job_application.interview_date,
                "application_date":job_application.application_date,
                "application_source":job_application.application_source,
                "status":job_application.status

            }

            return jsonify({'job': job_application_data})

        @app.route('/job_application', methods=['POST'])
        def create_job_application():

            data = request.get_json()


            job_application = self.model(

                    user_id =data['user_id'],
                    job_id =data['job_id'],
                    interview_date = data['interview_date'],
                    application_date=data['application_date'],
                    application_source=data['application_source'],
                    status=data['status']

                    )
            
            self.db.session.add(job_application)
            self.db.session.commit()

            return jsonify({'message': 'new job_application created'})
        

        @app.route('/job_application/<user_id>/<job_id>', methods=['PUT'])
        def update_job_application(user_id, job_id):


            data: dict = request.get_json()
            
            job_application = self.model().query.filter_by(user_id=user_id, job_id=job_id).first()

            
            self.db.session.add(job_application)
            self.db.session.commit()

            return jsonify({'message': 'new job_application created'})
        
        @app.route('/job_application/status/update/<user_id>/<job_id>', methods=['PUT'])
        def update_status_job_application(user_id, job_id):

            data: dict = request.get_json()

            job_application = self.model().query.filter_by(user_id=user_id, job_id=job_id).first()

            job_application.status = data['status']
            
            self.db.session.commit()

            def get_job_application_handler_mailing_list():
                
                handlers = self.user_model.query.filter_by(handles_job_applications=True)
                
                return [handler.email for handler in handlers]
            
            def create_formatted_inquiry(data: dict, address: str, user: object, job: object, status) -> EmailMessage:

                # create a formatted subject line for emails created by this backend
                # format a string for the fullname of the user
                # append it and the inquiry's subject, i_subject, to an optiflow message
                # output the formatted subject
                u_fullname = f'{user.surname}, {user.givenname}'
                subject = f'Optiflow | Job Application Status Change | {u_fullname} | {job.jobTitle}'

                content : str = ""

                formatted_content : str = create_formatted_content(u_fullname) 

                # initialize email; set from, to, subject, content 
                email = EmailMessage()
                email['Subject'] = subject
                email['From'] = environ.get('OPTIFLOW_ACCOUNTNAME')
                email['To'] = address
                email.set_content(formatted_content)

                return email
            
            def create_formatted_content(username: str) -> str:
                return f"""

                Good Day, {username}

                Your Job Status has changed to {job_application.status}. 

                Thank You

                """

            user = self.user_model().query.filter_by(id=user_id).first()
            job = self.job_model().query.filter_by(id=job_id).first()

            if not user:
                return jsonify({'message': 'No user found'})
            
            context = ssl.create_default_context()

            with SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:

                smtp.login(environ.get('OPTIFLOW_ACCOUNTNAME'), environ.get('OPTIFLOW_PASSWORD'))

                address_list : str = get_job_application_handler_mailing_list()

                address_list.append(user.email)

                status = job_application.status 

                for address in address_list:

                    data = request.get_json()

                    email = create_formatted_inquiry(data, address, user, job, status)

                    smtp.sendmail(

                              environ.get('OPTIFLOW_ACCOUNTNAME'),
                              address,
                              email.as_string()
                              
                    )

            return jsonify({'message': "email sent!"})

            return jsonify({'message': 'new job_application created'})

        @app.route('/job_application/<user_id>/<job_id>', methods=['DELETE'])
        def delete_job_application(user_id, job_id):

            job_application = self.model().query.get((user_id, job_id))

            if not job_application:
                return jsonify({'message': 'No user found'})
    

            self.db.session.delete(job_application)
            self.db.session.commit()

            return jsonify({'message': 'job has been deleted'})
        
        # CONSIDER USING DECORATORS LATER ON IF YOU NEED TO IMPROVE THIS
        @app.route('/job_application/notify/<user_id>/<job_id>', methods=['POST'])
        def send_job_application_email(user_id, job_id):

            job_application = self.model().query.get((user_id, job_id))


            if not job_application:
                return jsonify({'message': 'No user found'})
            
            user = self.user_model().query.filter_by(id=user_id).first()
            job = self.job_model().query.filter_by(id=job_id).first()
            
            def get_job_application_handler_mailing_list():
                
                handlers = self.user_model.query.filter_by(handles_job_applications=True)
                
                return [handler.email for handler in handlers]
            
            def create_formatted_inquiry(data: dict, address: str, user: object, job: object) -> EmailMessage:

                # create a formatted subject line for emails created by this backend
                # format a string for the fullname of the user
                # append it and the inquiry's subject, i_subject, to an optiflow message
                # output the formatted subject
                u_fullname = f'{user.surname}, {user.givenname}'
                subject = f'Optiflow | Job Application | {u_fullname} | {job.jobTitle}'

                formatted_content : str = create_formatted_content(u_fullname) 

                # initialize email; set from, to, subject, content 
                email = EmailMessage()
                email['Subject'] = subject
                email['From'] = environ.get('OPTIFLOW_ACCOUNTNAME')
                email['To'] = address
                email.set_content(formatted_content)

                return email
            
            def create_formatted_content(fullname: str) -> str:
                return f"""

                Good Day, {fullname}

                Your Job Application Has been sent for review. 
                We will return to you as soon as possible with our response.
                MGHS thanks you for your interest in {job.jobTitle} and we hope for your continued interest.

                Thank You

                """



            if not user:
                return jsonify({'message': 'No user found'})
            
            context = ssl.create_default_context()

            with SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:

                smtp.login(environ.get('OPTIFLOW_ACCOUNTNAME'), environ.get('OPTIFLOW_PASSWORD'))

                address_list : list = get_job_application_handler_mailing_list()


                for address in address_list:

                    data = request.get_json()

                    email = create_formatted_inquiry(data, address, user, job)

                    smtp.sendmail(

                              environ.get('OPTIFLOW_ACCOUNTNAME'),
                              address,
                              email.as_string()
                              
                    )

            return jsonify({'message': "email sent!"})
