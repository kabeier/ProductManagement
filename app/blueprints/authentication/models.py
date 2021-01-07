import base64, os, ast
from app import db
from datetime import datetime as dt
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    role_id=db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        self.password = generate_password_hash(original_password)

    def check_hashed_password(self, original_password):
        return check_password_hash(self.password, original_password)

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    create = db.Column(db.Boolean(), default=False)
    delete = db.Column(db.Boolean(), default=False)
    modify = db.Column(db.Boolean(), default=False)
    
    def from_dict(self, data):
        for field in ['name', 'create', 'delete', 'modify']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        role={
            "id":self.id,
            "name":self.name,
            "create":self.create,
            "delete":self.delete,
            "modify":self.modify,
        }
        return role