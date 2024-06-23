import os
from datetime import datetime

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from src.conf import settings
from src.data.history import PostgresHistory
from src.dep.postgres import get_postgres
from src.services.llm_service import LLMConversationService

ID_TO_NAME = {
    566572635: "Саша 1",
    405373776: "Рома",
    402112818: "Никита",
    128404397: "Андрей",
}


class TextSerivce:
    def __init__(self):
        self.conversation_service = LLMConversationService()
        self.pg_conn = get_postgres()

    def text_chat_history(
        self, chat_id: str, user_id: str, text: str, msg_date: datetime = None
    ):
        # try:
        user_id = str(user_id)
        chat_id = str(chat_id)

        history = PostgresHistory(user_id, chat_id, self.pg_conn)
        self.conversation_service.init_conversation_buffer(history)
        prediction = self.conversation_service.generate_response_for_history(text)
        reply_msg = prediction['response']
        # except Exception as ex:
        #     logger.error(ex)
        #     reply_msg = "😿"
        return reply_msg

    def single_message_predict(
        self, chat_id: str, user_id: str, text: str, msg_date: datetime
    ):
        # try:
        user_id = str(user_id)
        chat_id = str(chat_id)
        prediction = self.conversation_service.predict_single(text)
        reply_msg = prediction['response']
        # except Exception as ex:
        #     logger.error(ex)
        #     reply_msg = "😿"
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

    def show_chat_history(self, chat_id: str, user_id: str) -> list[str]:
        user_id = str(user_id)
        chat_id = str(chat_id)
        chat_history = PostgresHistory(user_id, chat_id, get_postgres())
        return "\n\n".join([msg.content for msg in chat_history.messages])

    def history_summary(self, chat_id: str, user_id: str) -> str:
        user_id = str(user_id)
        chat_id = str(chat_id)

        history = PostgresHistory(user_id, chat_id, get_postgres())
        self.conversation_service.init_conversation_buffer(history)
        prediction = self.conversation_service.summary()
        reply_msg = prediction['response']

        return reply_msg

    def search_agent_service(self, user_id: str, text: str, msg_date: datetime):
        ...

    def drop_context(self, chat_id: str, user_id: str, text: str, msg_date: datetime):
        user_id = str(user_id)
        chat_id = str(chat_id)
        history = PostgresHistory(user_id, chat_id, self.pg_conn)
        history.clear()
        return "Context dropped!"
