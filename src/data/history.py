import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Sequence

from langchain.schema import (
    AIMessage,
    BaseChatMessageHistory,
    HumanMessage,
    SystemMessage,
)
from langchain.schema.messages import BaseMessage, messages_from_dict, messages_to_dict
from loguru import logger

from src.conf import Role, settings
from src.services.message_service import MessageService


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, user_id: str, session_id: int = None):
        self.storage_path = 'data/history'
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
    def __init__(self, user_id: str, chat_id: str, pg_conn):
        self.user_id = user_id
        self.session_id = chat_id
        self.postgres = MessageService(pg_conn)

    @property
    def messages(self):
        messages_postgres = self.postgres.get_filtered_messages(
            chat_id=self.session_id, limit=settings.chat.max_history_len
        )
        messages_langchain = []
        for message in messages_postgres:
            match message.role:
                case Role.SYSTEM:
                    messages_langchain.append(
                        SystemMessage(
                            content=message.message,
                            additional_kwargs={
                                "type": "system",
                                "timestamp": message.datetime,
                            },
                        )
                    )
                case Role.USER:
                    messages_langchain.append(
                        HumanMessage(
                            content=message.message,
                            additional_kwargs={
                                "type": "text",
                                "timestamp": message.datetime,
                            },
                        )
                    )
                case Role.AI:
                    messages_langchain.append(
                        AIMessage(
                            content=message.message,
                            additional_kwargs={
                                "type": "text",
                                "timestamp": message.datetime,
                            },
                        )
                    )
        return messages_langchain

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        for message in messages:
            match message.type:
                case "system":
                    role = Role.SYSTEM
                case "human":
                    role = Role.USER
                case "ai":
                    role = Role.AI
                case _:
                    role = Role.USER

            self.postgres.add_message(
                self.session_id, self.user_id, message.content, role, datetime.now()
            )

    def clear(self):
        self.postgres.clear_messages()
