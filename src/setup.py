from main import app, db, User
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

from datetime import datetime

import uuid

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
                    email="test.joe@test.com"
                    )


    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        
        db.create_all()


        # try to create admin user
        # if admin user alraedy exists print message
        try:
            create_default_admin_user(db)
            print("created admin user")

        except:
            print("already created")