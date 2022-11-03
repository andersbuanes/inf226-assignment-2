from typing import List
from models import Message, User
from database import db

class DataHandler():
    def get_messages(self) -> List[Message]:
        #return db.session.query(db.select(Message)).all()
        return Message.query.all()

    def get_users(self) -> List[User]:
        return User.query.all()
    

    def get_search(self, query) -> List[Message]:
        return db.session.execute(db.select(Message).filter_by(message=query)).scalars()
    
    def add_user(self, username, password) -> None:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()


    def post_message(self, authenticated_user: User, content, recipient_ids) -> None:
        msg = Message(
            sender=authenticated_user.id,
            content=content,
            recipient_ids=recipient_ids
        )
        db.session.add(msg)
        db.session.commit()

