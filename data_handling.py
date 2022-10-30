from models import Announcement, Message
from app import db

class DataHandler():
    def get_messages(self):
        #return db.session.query(db.select(Message)).all()
        return Message.query.all()

    def get_search(self, query):
        return db.session.execute(db.select(Message).filter_by(message=query)).scalars()

    def get_announcments(self):
        return db.session.execute(db.select(Announcement)).scalars()

    def post_simple_message(self, sender, message):
        message = Message(
            sender=sender,
            message=message,
        )
        db.session.add(message)
        db.session.commit()

