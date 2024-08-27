from main import app, db, User
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

from datetime import datetime

import uuid

from os import environ

# This sets up the default admin user to log into the system.
def create_default_admin_user(db: SQLAlchemy):
    

    hashed_password = generate_password_hash('admin_password', method='pbkdf2:sha256')

    admin_user = User(
                    public_id=str(uuid.uuid4()),
                    givenname="John",
                    surname="Doe",
                    password=hashed_password,
                    admin=True,
                    username="admin",
                    phone_number="",
                    register_date=datetime.now().date(),
                    dob="2001-1-1",
                    email="test.joe@test.com",
                    handles_inquiries=True,
                    handles_job_applications=True
                    )


    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":


    # CREATE A COMMA SEPARATED LIST OF MGHS EMAILS WHICH SHOULD RECIEVE NOTIFICATIONS OF NEW JOB APPLICATIONS
    environ['JOB_APPLICANT_EMAIL_ADDRESS_LIST'] = "k.nitta.it@gmail.com"

    # CREATE A COMMA SEPARATED LIST OF MGHS EMAILS WHICH SHOULD RECIEVE NOTIFICATIONS OF INQUIRIES
    environ['INQUIRY_EMAIL_ADDRESS_LIST'] = "k.nitta.it@gmail.com"

    # SET UP ENVIRONMENT VARIABLES FOR THE GMAIL ACCOUNT
    environ['OPTIFLOW_ACCOUNTNAME'] = "optiflow.mghs@gmail.com"
    environ['OPTIFLOW_PASSWORD'] = "mhzz opbh fpdf kxgh"


    with app.app_context():
        
        db.create_all()


        # try to create admin user
        # if admin user alraedy exists print message
        try:
            create_default_admin_user(db)
            print("created admin user")

        except:
            print("already created")