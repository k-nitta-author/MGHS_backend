from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL
import ssl

from os import environ

class InquiryResource:

    def __init__(self, app: Flask, db: SQLAlchemy, user: object) -> None:
        
        self.register_routes(app, db)
        self.sender = user
        self.db = db

    def register_routes(self, app: Flask, db: SQLAlchemy) -> None:




        @app.route('/inquiry/<id>/<job_id>/send', methods=['POST'])
        def sendJobApplication(id, job_id):
            pass

        """
        EXAMPLE REQUEST FORMAT
        ----------------
        {
            "subject": "on the topic of diamonds",
            "body": "Lorem Ipsum",
        }
        """
        @app.route('/inquiry/<id>/send', methods=['POST'])
        def sendInquiry(id):


            def create_formatted_inquiry(data: dict, address: str, user: object) -> EmailMessage:

                # create a formatted subject line for emails created by this backend
                # format a string for the fullname of the user
                # append it and the inquiry's subject, i_subject, to an optiflow message
                # output the formatted subject
                u_fullname = f"{user.surname}, {user.givenname}"
                i_subject = data['subject']
                final_subject = f"Optiflow | Inquiry | {u_fullname} | {i_subject}" 


                content : str = data['body']

                formatted_content : str = create_formatted_content(content) 

                # initialize email; set from, to, subject, content 
                email = EmailMessage()
                email['Subject'] = final_subject
                email['From'] = environ.get('OPTIFLOW_ACCOUNTNAME')
                email['To'] = address
                email.set_content(formatted_content)

                return email
            
            # TODO: ADD PROPER FORMATTING TO CONTENT
            # add a simple header to content that indicates the source as OptiFlow
            # return the content with this header
            def create_formatted_content(body: str) -> str:
                return body

            user = self.sender().query.filter_by(id=id).first()

            if not user:
                return jsonify({'message': 'No user found'})
            
            context = ssl.create_default_context()

            with SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:

                smtp.login(environ.get('OPTIFLOW_ACCOUNTNAME'), environ.get('OPTIFLOW_PASSWORD'))

                address_list : str = environ.get('JOB_APPLICANT_EMAIL_ADDRESS_LIST').split(',')

                for address in address_list:

                    data = request.get_json()

                    email = create_formatted_inquiry(data, address, user)

                    smtp.sendmail(

                              environ.get('OPTIFLOW_ACCOUNTNAME'),
                              address,
                              email.as_string()
                              
                    )

            return jsonify({'message': "email sent!"})


