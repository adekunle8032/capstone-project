from flask import Flask
from database import db
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
#from sqlalchemy.orm import Session as DBSession
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the session
#db_session = DBSession()
#pp.config['SESSION_SQLALCHEMY'] = db_session
#Session(app)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



from models import User  # Import User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from routes import app_routes
app.register_blueprint(app_routes)

if __name__ == '__main__':
    app.run()
