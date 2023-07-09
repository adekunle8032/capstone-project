from database import db
import os

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SECRET_KEY = 'Ku-2XGhDPL3TPqJUy8dco5WoELANJMZ6'


# Session
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY = db
    
    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@example.com'
    MAIL_PASSWORD = 'your_password_here'

    # Other Configuration Options
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # Additional Configurations...


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'your_production_secret_key_here'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite3'


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}