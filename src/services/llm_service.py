import os
import sys
from typing import Sequence

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.schema import BaseMessage
from langchain_core.prompts.prompt import PromptTemplate
from loguru import logger

from data.prompts import CONVERSATION_PROMPT, SUMMARY_PROMPT
from src.conf import settings
from src.data.history import FileChatMessageHistory
from src.dep.llm import get_saiga_llm_llamacpp
from src.models.conversation import BaseConversation
from src.models.models import BaseLLM


class LLMService:
    def __init__(self, llm: BaseLLM, conversation: BaseConversation):
        self.llm = llm
        self.conversation = conversation

    def generate_response_for_history(self, history: Sequence[BaseMessage]) -> str:
        for msg in history:
            # print(f"*** Message: {msg.content}, Type: {msg.type}""")
            if msg.type == "human":
                self.conversation.add_user_message(msg.content)
            elif msg.type == "ai":
                self.conversation.add_bot_message(msg.content)

        prompt = self.conversation.get_prompt()
        # logger.debug(f"Symbols in prompt: {len(prompt)}")

        return self.llm.predict(prompt)

    def predict_single(self, prompt: str) -> str:
        self.conversation.add_user_message(prompt)
        prompt = self.conversation.get_prompt()
        return self.llm.predict(prompt)


class LLMChainService:
    def __init__(self, chat_history: FileChatMessageHistory):
        self.history = chat_history

        self.llm = get_saiga_llm_llamacpp()
        self.conversation_sum_bufw = ConversationChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=CONVERSATION_PROMPT, input_variables=['history', 'input']
            ),
            memory=ConversationSummaryBufferMemory(
                llm=self.llm,
                max_token_limit=650,
                human_prefix='Человек',
                ai_prefix='ИИ',
                prompt=PromptTemplate(
                    template=SUMMARY_PROMPT, input_variables=['summary', 'new_lines']
                ),
                chat_memory=self.history,
            ),
        )

    def generate_response_for_history(self, text: str) -> str:
        print('**** Buffer:')
        print(self.conversation_sum_bufw.memory.buffer)

        if (
            self.llm.get_num_tokens_from_messages(self.history.messages)
            > settings.model.max_tokens * 0.75
        ):
            self.history.clear()
            self.conversation_sum_bufw.memory.clear()

        return self.conversation_sum_bufw.invoke(text)

    def predict_single(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
