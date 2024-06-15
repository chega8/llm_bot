import json
import os
from datetime import datetime
from typing import Dict, List, Sequence

from langchain.schema import (
    AIMessage,
    BaseChatMessageHistory,
    HumanMessage,
    SystemMessage,
)
from langchain.schema.messages import BaseMessage, messages_from_dict, messages_to_dict
from loguru import logger

from src.db.repository import MessageRepository
from src.db.schema import Message
from src.dep.postgres import get_postgres
from src.services.message_service import MessageService


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, storage_path: str, user_id: int, session_id: str = None):
        self.storage_path = storage_path
        self.user_id = user_id
        if session_id is None:
            session_id = str(user_id)

        self.session_id = session_id

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.file_path = os.path.join(self.storage_path, self.session_id) + ".json"

    @property
    def messages(self):
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r") as f:
                messages = json.loads(f.read())
                return messages_from_dict(messages)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def _message_to_dict(message: BaseMessage) -> dict:
        return {"type": message.type, "data": message.dict()}

    def messages_to_dict(self, messages: Sequence[BaseMessage]) -> Dict[str, dict]:
        return {
            f"History.{m.additional_kwargs.get('timestamp')}": self._message_to_dict(m)
            for m in messages
        }

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        logger.debug(
            f"Adding messages, the last one: {all_messages[-1].content}, role: {all_messages[-1].type}"
        )

        serialized = messages_to_dict(all_messages)
        with open(self.file_path, "w") as f:
            json.dump(serialized, f)

    def clear(self):
        if self.file_path is not None and os.path.exists(self.file_path):
            os.remove(self.file_path)
        else:
            return
        with open(self.file_path, "w") as f:
            f.write("[]")


class PostgresHistory(BaseChatMessageHistory):
    def __init__(self, user_id: int, session_id: str = None):
        self.user_id = user_id
        if session_id is None:
            session_id = str(user_id)

        self.session_id = session_id
        self.postgres = MessageService(get_postgres())

    @property
    def messages(self):
        messages_postgres = self.postgres.get_all_messages()
        messages_langchain = []
        for message in messages_postgres:
            if message.role == "system":
                messages_langchain.append(
                    SystemMessage(
                        content=message.message,
                        additional_kwargs={
                            "type": "system",
                            "timestamp": int(message.datetime),
                        },
                    )
                )
            elif message.role == "human":
                messages_langchain.append(
                    HumanMessage(
                        content=message.message,
                        additional_kwargs={
                            "type": "text",
                            "timestamp": int(message.datetime),
                        },
                    )
                )
            elif message.role == "ai":
                messages_langchain.append(
                    AIMessage(
                        content=message.message,
                        additional_kwargs={
                            "type": "text",
                            "timestamp": int(message.datetime),
                        },
                    )
                )

        return messages_langchain

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        for message in messages:
            self.postgres.add_message(
                self.session_id, self.user_id, message.content, datetime.now()
            )

    def clear(self):
        self.postgres.clear_messages()
