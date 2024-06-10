import os
from datetime import datetime

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from src.data.history import FileChatMessageHistory, MongoDBChatMessageHistory
from src.data.utils import merge_all_files
from src.models.conversation import SaigaConversation
from src.models.models import SaigaLLM
from src.services.llm_service import LLMService


def text_chat_service(user_id: int, text: str, msg_date: datetime):
    # try:
    chat_history = FileChatMessageHistory("data/history", user_id)
    # await chat_history.clear()

    llm = SaigaLLM()
    conversation = SaigaConversation()
    llm_service = LLMService(llm, conversation)

    messages = chat_history.messages
    for message in messages:
        logger.debug(f"Message: {message.content}")
    logger.debug(f"History hessages count: {len(messages)}")

    new_messages = []
    if len(messages) == 0:
        new_messages.append(
            SystemMessage(
                content=conversation.system_prompt,
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

    # Already have system prompt inside conversation instance
    ai_response = llm_service.generate_response_for_history(new_messages)

    new_messages.append(
        AIMessage(
            content=ai_response,
            additional_kwargs={
                "type": "text",
                "timestamp": int(msg_date.timestamp()) + 10,
            },
        )
    )
    chat_history.add_messages(new_messages)

    reply_msg = ai_response
    # except Exception as ex:
    #     logger.error(ex)
    #     reply_msg = "😿"
    return reply_msg


def single_message_predict(user_id: int, text: str, msg_date: datetime):
    try:
        llm = SaigaLLM()
        conversation = SaigaConversation()
        llm_service = LLMService(llm, conversation)

        ai_response = llm_service.predict_single(text)

        reply_msg = ai_response
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
