import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime

import pytest
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from src.data.history import FileChatMessageHistory
from src.dep.mongo import get_mongo


def test_init():
    f = FileChatMessageHistory("test/data/history", 1)
    assert f


def test_add_message():
    f = FileChatMessageHistory("test/data/history", 1)
    f.clear()

    sys_msg = SystemMessage(
        content="test system prompt",
        additional_kwargs={
            "type": "system",
            "timestamp": int(datetime.now().timestamp()),
        },
    )

    hum_msg = HumanMessage(
        content="Test Human Message",
        additional_kwargs={
            "type": "text",
            "timestamp": int(datetime.now().timestamp()),
        },
    )

    f.add_messages([sys_msg, hum_msg])
    assert len(f.messages) == 2

    f.add_messages([sys_msg, hum_msg])
    assert len(f.messages) == 4

    print([m.content for m in f.messages])
    print([m.type for m in f.messages])

    f.clear()
    assert len(f.messages) == 0
