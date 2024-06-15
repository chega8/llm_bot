from sqlalchemy.orm import Session

from conf import Role
from src.db.repository import MessageRepository


class MessageService:
    def __init__(self, db: Session):
        self.repository = MessageRepository(db)

    def add_message(self, chat_id: str, user_id: str, message: str, datetime):
        return self.repository.insert_message(chat_id, user_id, message, datetime)

    def get_all_messages(self):
        return self.repository.get_messages()

    def get_filtered_messages(
        self, chat_id: str = None, user_id: str = None, role: Role = None, datetime=None
    ):
        return self.repository.get_messages_by_filter(chat_id, user_id, role, datetime)

    def clear_messages(self):
        return self.repository.clear_messages()
