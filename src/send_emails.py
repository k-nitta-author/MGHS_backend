from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL
import ssl
from os import environ

def send_email(mailing_list_function: function, create_body_function):

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