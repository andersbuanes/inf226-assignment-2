from app import db
from flask_login import UserMixin

class User(UserMixin, db.model):
    __bind_key__ = 'auth'
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=True, nullable=False)
    
    def __repr__(self):
        return "<User %r>" % self.username
    
class Message(db.Model):
    __bind_key__ = 'content'
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500), nullable=False)