import os
from datetime import datetime

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from src.data.history import FileChatMessageHistory, MongoDBChatMessageHistory
from src.data.utils import merge_all_files
from src.models import SaigaConversation, SaigaLLM


def text_chat_service(user_id: int, text: str, msg_date: datetime):
    try:
        chat_history = FileChatMessageHistory("data/history", user_id)
        # await chat_history.clear()

        llm = SaigaLLM()
        conversation = SaigaConversation(system_prompt=llm.system_prompt)

        messages = chat_history.messages
        new_messages = []
        if not messages:
            new_messages.append(
                SystemMessage(
                    content=llm.system_prompt,
                    additional_kwargs={
                        "type": "system",
                        "timestamp": int(msg_date.timestamp()) - 10,
                    },
                )
            )
        new_messages.append(
            HumanMessage(
                content=text,
                additional_kwargs={
                    "type": "text",
                    "timestamp": int(msg_date.timestamp()),
                },
            )
        )

        llm_inputs = [msg.content for msg in messages + new_messages]
        conversation.add_user_message(llm_inputs)
        logger.info(f"Symbols in prompty: {len(conversation.get_prompt())}")

        response = llm.predict_conversation(conversation)

        new_messages.append(
            AIMessage(
                content=response,
                additional_kwargs={
                    "type": "text",
                    "timestamp": int(msg_date.timestamp()) + 10,
                },
            )
        )
        chat_history.add_messages(new_messages)

        reply_msg = response
    except Exception as ex:
        logger.error(ex)
        reply_msg = "😿"
    return reply_msg


def full_history_predict(user_id: int, text: str, msg_date: datetime):
    try:
        llm = SaigaLLM()
        conversation = SaigaConversation(system_prompt=llm.system_prompt)

        chat_history = merge_all_files()
        chat_history.append(text)
        for msg in chat_history:
            conversation.add_user_message(msg)

        logger.info(f"Symbols in prompty: {len(conversation.get_prompt())}")

        response = llm.predict(conversation)
        reply_msg = response
    except Exception as ex:
        logger.error(ex)
        reply_msg = "😿"
    return reply_msg
