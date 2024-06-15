from sqlalchemy.orm import Session

from conf import Role
from src.db.schema import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_message(
        self, chat_id: str, user_id: str, message: str, role: Role, datetime
    ):
        db_message = Message(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            role=role,
            datetime=datetime,
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_messages(self):
        return self.db.query(Message).all()

    def get_messages_by_filter(
        self, chat_id: str = None, user_id: str = None, role: Role = None, datetime=None
    ):
        query = self.db.query(Message)
        if chat_id:
            query = query.filter(Message.chat_id == chat_id)
        if user_id:
            query = query.filter(Message.user_id == user_id)
        if datetime:
            query = query.filter(Message.datetime == datetime)
        if role:
            query = query.filter(Message.role == role)
        return query.all()

    def clear_messages(self):
        self.db.query(Message).delete()
        self.db.commit()
