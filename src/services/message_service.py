from sqlalchemy.orm import Session

from src.conf import Role
from src.db.repository import MessageRepository
from src.db.schema import Message


class MessageService:
    def __init__(self, db: Session):
        self.repository = MessageRepository(db)

    def add_message(
        self, chat_id: str, user_id: str, message: str, role: Role, datetime
    ):
        return self.repository.insert_message(chat_id, user_id, message, role, datetime)

    def get_all_messages(self) -> list[Message]:
        return self.repository.get_messages()

    def get_filtered_messages(
        self,
        chat_id: str = None,
        user_id: str = None,
        role: Role = None,
        datetime=None,
        limit: int = None,
    ):
        return self.repository.get_messages_by_filter(
            chat_id=chat_id, user_id=user_id, role=role, datetime=datetime, limit=limit
        )

    def clear_messages(self, chat_id: str):
        return self.repository.clear_messages(chat_id)
