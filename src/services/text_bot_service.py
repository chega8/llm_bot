import os
import re
from datetime import datetime

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from src.conf import settings
from src.data.history import PostgresHistory
from src.db.repository import ToxRepository
from src.dep.postgres import get_postgres
from src.services.conversation_service import (
    LLMConversationService,
    LLMConversationServicev2,
)
from src.services.summary_service import SummaryService

ID_TO_NAME = {
    566572635: "Саша 1",
    405373776: "Рома",
    402112818: "Никита",
    128404397: "Андрей",
}


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(ex)
            return "😿"

    return wrapper


class TextSerivce:
    def __init__(self):
        self.conversation_service = LLMConversationService()
        self.summary_service = SummaryService()
        self.pg_conn = get_postgres()

    @error_handler
    def text_chat_history(
        self, chat_id: str, user_id: str, text: str, msg_date: datetime = None
    ):
        user_id = str(user_id)
        chat_id = str(chat_id)

        text = text.strip().replace("/chat ", "")

        history = PostgresHistory(user_id, chat_id, self.pg_conn)
        self.conversation_service.init_conversation_buffer(history)
        prediction = self.conversation_service.chat(text)
        reply_msg = prediction['response']
        return reply_msg

    @error_handler
    def single_message_predict(
        self, chat_id: str, user_id: str, text: str, msg_date: datetime
    ):
        text = text.replace('/msg', '')
        reply_msg = self.conversation_service.message(text)
        # reply_msg = prediction['response']
        return reply_msg

    def collect_chat_history(
        self, chat_id: str, user_id: str, text: str, msg_date: datetime
    ):
        user_id = str(user_id)
        chat_id = str(chat_id)
        history = PostgresHistory(user_id, chat_id, self.pg_conn)

        messages = [
            HumanMessage(
                content=text.replace("/chat ", ""),
                additional_kwargs={
                    "type": "text",
                    "timestamp": msg_date,
                },
            )
        ]
        history.add_messages(messages)

    def show_chat_history(self, chat_id: str, user_id: str) -> str:
        user_id = str(user_id)
        chat_id = str(chat_id)
        chat_history = PostgresHistory(user_id, chat_id, self.pg_conn)
        return "\n".join([msg.content for msg in chat_history.messages])

    def history_summary(self, chat_id: str, user_id: str, text) -> str:
        user_id = str(user_id)
        chat_id = str(chat_id)

        history = PostgresHistory(user_id, chat_id, self.pg_conn)
        reply_msg = self.summary_service.summarize_history(history)

        text = text.replace('/summary', '')
        if len(text) > 1:
            text = 'summary: {}\nuser: {}\nai: '.format(reply_msg, text)

            print(text)
            reply_msg = self.conversation_service.message(text)
        return reply_msg

    def toxic_predict(self, chat_id: str, user_id: str, text: str) -> str:
        text = text.replace('/tox', '')
        prediction = self.conversation_service.toxicity(text)

        pattern = re.compile(r"токсичность: (\d+)%")
        match = pattern.search(prediction)

        if match:
            toxicity = int(match.group(1))

            rep = ToxRepository(self.pg_conn)

            rep.insert_message(chat_id, user_id, message=text, tox=toxicity)
            if toxicity > 30:
                return f"Токсичность: {toxicity}%"

    def search_agent_service(self, user_id: str, text: str, msg_date: datetime):
        ...

    def drop_context(self, chat_id: str, user_id: str, text: str, msg_date: datetime):
        user_id = str(user_id)
        chat_id = str(chat_id)
        history = PostgresHistory(user_id, chat_id, self.pg_conn)
        history.clear()
        return "Context dropped!"


class TextSerivcev2:
    def __init__(self):
        self.conversation_service = LLMConversationServicev2()
        self.pg_conn = get_postgres()

    # @error_handler
    def text_chat_history(
        self, chat_id: str, user_id: str, text: str, msg_date: datetime = None
    ):
        user_id = str(user_id)
        chat_id = str(chat_id)

        response = self.conversation_service.with_message_history.invoke(
            {"input": text},
            config={
                "configurable": {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "conn": self.pg_conn,
                }
            },
        )
        return response
