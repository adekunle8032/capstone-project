from passlib.hash import bcrypt_sha256
from database import db
from models import User
from flask import Flask

# Create Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ... other app configurations

# Initialize the database
db.init_app(app)

# Create an application context
with app.app_context():
    # Fetch all users from the database
    users = User.query.all()

    # Update the password hashes for each user
    for user in users:
        # Assuming the User model has a 'password_hash' attribute instead of 'password'
        user.password_hash = bcrypt_sha256.hash(user.password_hash)

    # Commit the changes to the database
    db.session.commit()
