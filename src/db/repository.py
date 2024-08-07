from datetime import datetime

from sqlalchemy.orm import Session

from src.conf import Role
from src.db.schema import Message, Tox


class MessageRepository:
    def __init__(self, db: Session, schema=Message):
        self.db = db
        self.schema = schema

    def insert_message(
        self, chat_id: str, user_id: str, message: str, role: Role, dt=datetime.now()
    ):
        db_message = self.schema(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            role=role,
            datetime=dt,
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_messages(self) -> list[Message]:
        return self.db.query(self.schema).all()

    def get_messages_by_filter(
        self,
        chat_id: str = None,
        user_id: str = None,
        role: Role = None,
        dt=None,
        limit: int = None,
    ):
        query = self.db.query(self.schema)
        if chat_id:
            query = query.filter(self.schema.chat_id == chat_id)
        if user_id:
            query = query.filter(self.schema.user_id == user_id)
        if dt:
            query = query.filter(self.schema.datetime > dt)
        if role:
            query = query.filter(self.schema.role == role)
        if limit:
            query = query.order_by(self.schema.datetime.desc()).limit(limit)
            return query.all()[::-1]
        return query.all()

    def clear_messages(self, chat_id):
        self.db.query(self.schema).filter(self.schema.chat_id == chat_id).delete()
        self.db.commit()


class ToxRepository:
    def __init__(self, db: Session, schema=Tox):
        self.db = db
        self.schema = schema

    def insert_message(
        self, chat_id: str, user_id: str, message: str, tox: float, dt=datetime.now()
    ):

        db_message = self.schema(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            tox=tox,
            datetime=dt,
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_messages(self) -> list[Tox]:
        return self.db.query(self.schema).all()
