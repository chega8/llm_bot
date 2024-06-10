import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime

import pytest
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from src.data.history import FileChatMessageHistory
from src.models.conversation import BaseConversation


class MocConversation(BaseConversation):
    def __init__(
        self,
        system_prompt="Conversation System Prompt",
        message_template="<s>{role}\n{content}</s>",
        response_template="<s>bot\n",
    ):
        super().__init__(system_prompt, message_template, response_template)

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_bot_message(self, message):
        self.messages.append({"role": "bot", "content": message})

    def get_prompt(self):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += self.response_template
        return final_text.strip()


@pytest.fixture
def moc_system_message():
    return SystemMessage(
        content="Test system prompt",
        additional_kwargs={
            "type": "system",
            "timestamp": int(datetime.now().timestamp()),
        },
    )
    return system_message


@pytest.fixture
def moc_human_message():
    return HumanMessage(
        content="Test Human Message",
        additional_kwargs={
            "type": "text",
            "timestamp": int(datetime.now().timestamp()),
        },
    )
    return human_message


@pytest.fixture
def moc_ai_message():
    return AIMessage(
        content="Test AI Message",
        additional_kwargs={
            "type": "text",
            "timestamp": int(datetime.now().timestamp()),
        },
    )
    return ai_message


@pytest.fixture
def moc_history(moc_system_message, moc_human_message):
    chat_history = FileChatMessageHistory("test/data/history", 228)
    chat_history.clear()
    chat_history.add_messages([moc_system_message, moc_human_message])
    return chat_history


def test_histry(moc_history, moc_system_message, moc_human_message, moc_ai_message):
    assert len(moc_history.messages) == 2

    moc_history.add_messages([moc_ai_message])
    assert len(moc_history.messages) == 3
    assert moc_history.messages[-1].content == "Test AI Message"

    moc_history.add_messages([moc_human_message])
    assert len(moc_history.messages) == 4
    assert moc_history.messages[-1].content == "Test Human Message"


def test_conversation(moc_system_message, moc_human_message, moc_ai_message):
    conversation = MocConversation()

    conversation.get_prompt()
    assert (
        conversation.get_prompt()
        == """<s>system
Conversation System Prompt</s><s>bot"""
    )

    conversation.add_user_message(moc_human_message.content)
    assert (
        conversation.get_prompt()
        == f"""<s>system
Conversation System Prompt</s><s>user
{moc_human_message.content}</s><s>bot"""
    )

    conversation.add_user_message(moc_human_message.content)
    print(conversation.get_prompt())

    conversation.add_bot_message(moc_ai_message.content)
    print(conversation.get_prompt())
