from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
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

    def __repr__(self):
        return "<Message %r>" % self.message


class Announcement(db.Model):
    __bind_key__ = 'content'
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    auther = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return "<Announcement %r>" % self.text
