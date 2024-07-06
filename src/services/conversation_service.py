import os
import sys
from typing import Sequence

from src.data.history import InMemoryHistory, PostgresHistory
from src.dep.postgres import get_postgres

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chains.llm import LLMChain
from langchain.memory import (
    ChatMessageHistory,
    ConversationBufferMemory,
    ConversationSummaryMemory,
)
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from loguru import logger

from data.prompts import SUMMARY_PROMPT, mistral_saiga
from src.conf import settings
from src.dep.llm import get_saiga_llm_llamacpp

HISTORY_STORE = {}


class LLMConversationService:
    def __init__(self):
        self.history = None

        self.llm = get_saiga_llm_llamacpp()

    def chat(self, text: str) -> dict:
        # print('\n**** Buffer:')
        # print(self.conversation_sum_bufw.memory.buffer)

        text = text.strip().replace('/chat', '')

        if (
            self.llm.get_num_tokens_from_messages(self.history.messages)
            > (settings.model.ctx - settings.model.max_tokens) * 0.9
        ):
            self.conversation_chain.memory.clear()
            logger.info("Buffer cleared")

        return self.conversation_chain.invoke(text)

    def summary(self) -> str:
        messages = self.history.messages
        prompt = PromptTemplate(
            template=mistral_saiga["conversation_summary_prompt"],
            input_variables=['text'],
        )
        chain = prompt | self.llm
        text_messages = '\n'.join(
            [m.content for m in messages if isinstance(m, HumanMessage)]
        )
        logger.info(f"Text messages: {text_messages}")

        text_messages = text_messages[
            : (settings.model.ctx - settings.model.max_tokens) * 2.5
        ]
        return chain.invoke(text_messages)

    def set_args(self, chat_id: str, user_id: str, timestamp=None):
        self.history.session_id = chat_id
        self.history.user_id = user_id
        self.conversation_sum_bufw.memory.chat_memory.session_id = chat_id
        self.conversation_sum_bufw.memory.chat_memory.user_id = user_id

    def message(self, prompt: str) -> dict:
        messages = [
            SystemMessage(content=mistral_saiga["default_system_prompt"]),
            HumanMessage(content=prompt),
        ]
        return self.llm.invoke(messages)

    def init_conversation_buffer(self, history=None):
        self.history = history

        # mem = ConversationSummaryMemory.from_messages(
        #     llm=self.llm,
        #     chat_memory=self.history,
        #     return_messages=True,
        #     prompt=PromptTemplate(
        #         template=mistral_saiga["conversation_summary_prompt"],
        #         input_variables=['summary', 'new_lines'],
        #     )
        # )

        self.conversation_chain = ConversationChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=mistral_saiga["conversation_prompt"],
                input_variables=['history', 'input'],
            ),
            verbose=True,
            memory=ConversationBufferMemory(
                llm=self.llm,
                max_token_limit=650,
                human_prefix='Человек',
                ai_prefix='ИИ',
                chat_memory=history,
                verbose=True,
            ),
        )
        self.conversation_chain.llm.verbose = True

    def toxicity(self, text: str) -> str:
        prompt = PromptTemplate(
            template=mistral_saiga["toxic_clf_prompt"],
            input_variables=['text'],
        )
        chain = prompt | self.llm
        return chain.invoke(text)


class LLMConversationServicev2:
    def __init__(self):
        self.llm = get_saiga_llm_llamacpp()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им.",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        self.runnable = prompt | self.llm

        def get_session_history(
            user_id: str, chat_id: str, conn
        ) -> BaseChatMessageHistory:
            return InMemoryHistory()
            # if (user_id, chat_id) not in HISTORY_STORE:
            #     HISTORY_STORE[(user_id, chat_id)] = PostgresHistory(user_id, chat_id, conn)
            # return HISTORY_STORE[(user_id, chat_id)]

        self.with_message_history = RunnableWithMessageHistory(
            self.runnable,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="user_id",
                    annotation=str,
                    name="User ID",
                    description="Unique identifier for the user.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="chat_id",
                    annotation=str,
                    name="Conversation ID",
                    description="Unique identifier for the conversation.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="conn",
                    annotation=str,
                    name="pg conn",
                    description="pg conn",
                    is_shared=True,
                ),
            ],
        )
