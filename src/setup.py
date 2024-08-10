from main import app, db, User
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash
import uuid

# This sets up the default admin user to log into the system.
def create_default_admin_user(db: SQLAlchemy):
    

    hashed_password = generate_password_hash('admin_password', method='pbkdf2:sha256')

    admin_user = User(
                    public_id=str(uuid.uuid4()),
                    phone_number=None,
                    name="John Doe",
                    password=hashed_password,
                    admin=True,
                    username="admin"
                    )


    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        
        db.create_all()
        #create_default_admin_user(db)