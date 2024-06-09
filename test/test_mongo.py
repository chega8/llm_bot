import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest

from src.data.history import MongoDBChatMessageHistory
from src.dep.mongo import get_mongo


@pytest.fixture
def mongo_db():
    return MongoDBChatMessageHistory("test", 1)


# async def test_ping():
#     await get_mongo().ping()

# async def test_create_collection():
#     await get_mongo().client.drop_database("test")
#     await get_mongo().create_collection("test", "chats")
#     collection_names = await get_mongo().get_database("test").list_collection_names()
#     assert "chats" in collection_names


async def test_add_messages(mongo_db):
    messages = [
        {
            "type": "system",
            "data": {
                "content": "Hello",
                "additional_kwargs": {"type": "system", "timestamp": 1},
            },
        },
        {
            "type": "text",
            "data": {
                "content": "Hello",
                "additional_kwargs": {"type": "text", "timestamp": 2},
            },
        },
    ]
    mongo_db.add_messages(messages)
    messages = [msg async for k, v in mongo_db.messages for msg in v]
    assert len(messages) == 2
    assert messages[0].content == "Hello"
    assert messages[1].content == "Hello"
    mongo_db.clear()


async def test_clear(mongo_db):
    messages = [
        {
            "type": "system",
            "data": {
                "content": "Hello",
                "additional_kwargs": {"type": "system", "timestamp": 1},
            },
        },
        {
            "type": "text",
            "data": {
                "content": "Hello",
                "additional_kwargs": {"type": "text", "timestamp": 2},
            },
        },
    ]
    mongo_db.add_messages(messages)
    await mongo_db.clear()
    messages = [msg async for k, v in mongo_db.messages for msg in v]
    assert len(messages) == 0
