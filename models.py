from database import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, MetaData, String

join_table = 'recipients'

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(300), unique=True, nullable=False)

    def get_messages(self):
        return self.received_messages
    
    def __repr__(self):
        return "<User %r>" % self.received_messages
    
message_reciepent = db.Table(join_table,
                    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey(User.id)),
                    )

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    recipients = db.relationship(User, secondary=join_table, backref='received_messages')

    def __repr__(self):
        return f"<Message sent by {self.sender}  {self.content}>"
