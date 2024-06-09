import json
import os
from typing import Dict, List, Sequence

from langchain.schema import BaseChatMessageHistory
from langchain.schema.messages import BaseMessage, messages_from_dict, messages_to_dict
from loguru import logger
from pymongo import errors

from src.dep.mongo import get_mongo


class MongoDBChatMessageHistory(BaseChatMessageHistory):
    """Chat message history that stores history in MongoDB."""

    index_created: bool = False

    def __init__(self, database_name: str, user_id: int, session_id: str = None):
        self.db = get_mongo().get_database(database_name)
        self.collection = self.db["chats"]
        self.user_id = user_id
        self.session_id = session_id

    @staticmethod
    def _message_to_dict(message: BaseMessage) -> dict:
        return {"type": message.type, "data": message.dict()}

    def messages_to_dict(self, messages: Sequence[BaseMessage]) -> Dict[str, dict]:
        return {
            f"History.{m.additional_kwargs.get('timestamp')}": self._message_to_dict(m)
            for m in messages
        }

    async def setup(self):
        await self.collection.create_index(["user_id", "session_id"])

    @property
    async def messages(self):
        """Retrieve the messages from MongoDB"""
        filters = {"user_id": self.user_id}
        if self.session_id is not None:
            filters["session_id"] = self.session_id
        cursor = self.collection.find(filters)
        async for c in cursor:
            yield c.get("session_id"), messages_from_dict(
                list(c.get("History", {}).values())
            )

    async def add_messages(self, messages: List[BaseMessage]) -> None:
        try:
            await self.collection.update_one(
                {"user_id": self.user_id, "session_id": self.session_id},
                {"$set": self.messages_to_dict(messages)},
                upsert=True,
            )
        except errors.WriteError as err:
            logger.error(err)

    async def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in MongoDB"""
        await self.add_messages([message])

    async def remove_message(self, key: str) -> None:
        try:
            await self.collection.update_one(
                {"user_id": self.user_id, "session_id": self.session_id},
                {"$unset": {f"History.{key}": ""}},
                upsert=True,
            )
        except errors.WriteError as err:
            logger.error(err)

    async def clear(self) -> None:
        """Clear session memory from MongoDB"""
        try:
            await self.collection.delete_many({"user_id": self.user_id})
        except errors.WriteError as err:
            logger.error(err)


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
