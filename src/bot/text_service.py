import os
from datetime import datetime

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from data.prompts import CONVERSATION_PROMPT
from src.conf import settings
from src.data.history import FileChatMessageHistory
from src.models.conversation import MistralConversation, SaigaConversation
from src.models.models import SaigaLLM
from src.services.agent_service import AgentSearch
from src.services.llm_service import LLMChainService, LLMService

ID_TO_NAME = {
    566572635: "Саша 1",
    405373776: "Рома",
    402112818: "Никита",
    128404397: "Андрей",
}


def text_chat_service(user_id: int, text: str, msg_date: datetime):
    # try:
    chat_history = FileChatMessageHistory("data/history", user_id)
    # await chat_history.clear()

    llm_service = LLMChainService(chat_history)

    messages = chat_history.messages
    for message in messages:
        logger.debug(
            f"Message: {message.content}, type: {message.type}, user_id: {user_id}"
        )
    logger.debug(f"History hessages count: {len(messages)}, user_id: {user_id}")

    new_messages = []
    if len(messages) == 0:
        new_messages.append(
            SystemMessage(
                content=CONVERSATION_PROMPT,
                additional_kwargs={
                    "type": "system",
                    "timestamp": int(msg_date.timestamp()) - 10,
                },
            )
        )
    new_messages.append(
        HumanMessage(
            content=text.replace("/chat ", ""),
            additional_kwargs={
                "type": "text",
                "timestamp": int(msg_date.timestamp()),
            },
        )
    )

    ai_response = llm_service.generate_response_for_history(messages[1:] + new_messages)

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


def text_chat_history(chat_id, text: str, msg_date: datetime):
    chat_history = FileChatMessageHistory("data/history", chat_id)
    llm_service = LLMChainService(chat_history)
    ai_response = llm_service.generate_response_for_history(text.replace("/chat ", ""))
    reply_msg = ai_response['response']
    return reply_msg


def collect_chat_history(chat_id: int, user_id: int, text: str, msg_date: datetime):
    chat_history = FileChatMessageHistory("data/history", chat_id)
    messages = chat_history.messages

    name = ID_TO_NAME.get(user_id, "Unknown")
    text = name + ": " + text
    print('*****', text)
    msg = HumanMessage(
        content=text.replace("/chat ", ""),
        additional_kwargs={
            "type": "text",
            "timestamp": int(msg_date.timestamp()),
        },
    )
    messages.append(msg)

    if len(messages) > settings.chat.max_history_len:
        messages = messages[-settings.chat.max_history_len :]
        chat_history.clear()
        chat_history.add_messages(messages)
    else:
        chat_history.add_messages([msg])


def show_chat_history(chat_id: int) -> list[str]:
    chat_history = FileChatMessageHistory("data/history", chat_id)
    return "\n\n".join([msg.content for msg in chat_history.messages])


def single_message_predict(user_id: int, text: str, msg_date: datetime):
    try:
        chat_history = FileChatMessageHistory("data/history", user_id)
        llm_service = LLMChainService(chat_history)

        ai_response = llm_service.predict_single(text.replace("/msg ", ""))

        reply_msg = ai_response
    except Exception as ex:
        logger.error(ex)
        reply_msg = "😿"
    return reply_msg


def search_agent_service(user_id: int, text: str, msg_date: datetime):
    agent_service = AgentSearch()

    result = agent_service.search(text)
    return result


def drop_context(user_id: int):
    chat_history = FileChatMessageHistory("data/history", user_id)
    chat_history.clear()
