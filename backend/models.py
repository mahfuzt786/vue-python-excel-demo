# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     contact_number = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     role = db.Column(db.String(20), nullable=False, default='user')

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), default='user')

def create_default_admin():
    admin_email = 'admin@kic.com'
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            name='Admin',
            email=admin_email,
            # password=bcrypt.generate_password_hash('kic_admin12').decode('utf-8'),
            password='kic_admin12',
            address='Admin Address',
            contact_number='1234567890',
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
