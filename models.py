from database import db
from passlib.hash import bcrypt_sha256
import datetime
from flask_login import UserMixin
#from sqlalchemy import func
#from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    short_urls = db.relationship('ShortURL', backref='user', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.email = email

    def _hash_password(self, password):
        return bcrypt_sha256.hash(password)

    def check_password(self, password):
        return bcrypt_sha256.verify(password, self.password_hash)
    
    def get_id(self):
        return str(self.id)

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    custom_url = db.Column(db.String(255), nullable=True)  # Add the custom_url column
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    link_analytics = db.relationship('LinkAnalytics', backref='short_url', lazy=True)
    custom_urls = db.relationship('CustomURL', backref='short_url', lazy=True)


class LinkAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey('short_url.id', name='fk_linkanalytics_short_url'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, short_url_id, ip_address, country=None, city=None):
        self.short_url_id = short_url_id
        self.ip_address = ip_address
        self.country = country
        self.city = city
        
    #@staticmethod
    #def get_visit_counts(short_url_id):
     #   return LinkAnalytics.query.filter_by(short_url_id=short_url_id).count()


class CustomURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey('short_url.id'), nullable=False)
    custom_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, short_url_id, custom_code):
        self.short_url_id = short_url_id
        self.custom_code = custom_code
        
from app import login_manager
        
#@login_manager.user_loader
#def load_user(user_id):
 #   return Session.get(User, int(user_id))
