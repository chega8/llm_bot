import os
import sys
from typing import Sequence

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain.chains import ConversationChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import BaseChatMessageHistory, BaseMessage
from langchain_core.prompts import PromptTemplate
from loguru import logger

from data.prompts import SUMMARY_PROMPT, mistral_saiga
from src.conf import settings
from src.dep.llm import get_saiga_llm_llamacpp


class LLMConversationService:
    def __init__(self):
        self.history = None

        self.llm = get_saiga_llm_llamacpp()
        self.llm_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(mistral_saiga["default_system_prompt"]),
        )
        self.summary_chain = LLMChain(
            llm=self.llm, prompt=PromptTemplate.from_template(SUMMARY_PROMPT)
        )

    def generate_response_for_history(self, text: str) -> str:
        # print('\n**** Buffer:')
        # print(self.conversation_sum_bufw.memory.buffer)

        if (
            self.llm.get_num_tokens_from_messages(self.history.messages)
            > (settings.model.ctx - settings.model.max_tokens) * 0.9
        ):
            self.conversation_sum_bufw.memory.clear()
            logger.info("Buffer cleared")

        return self.conversation_sum_bufw.invoke(text)

    def summary(self) -> str:
        messages = self.history.messages
        inp = "\n".join([f"{msg.type}: {msg.content}" for msg in messages[1:]])
        logger.info(f"Summary input: {inp[:100]}")
        # return self.summary_chain.invoke(inp)
        return self.summary_chain.invoke(messages)

    def set_args(self, chat_id: str, user_id: str, timestamp=None):
        self.history.session_id = chat_id
        self.history.user_id = user_id
        self.conversation_sum_bufw.memory.chat_memory.session_id = chat_id
        self.conversation_sum_bufw.memory.chat_memory.user_id = user_id

    def predict_single(self, prompt: str) -> str:
        return self.llm_chain.invoke(prompt)

    def init_conversation_buffer(self, history=None):
        self.history = history
        self.conversation_sum_bufw = ConversationChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=mistral_saiga["conversation_prompt"],
                input_variables=['history', 'input'],
            ),
            verbose=True,
            memory=ConversationSummaryBufferMemory(
                llm=self.llm,
                max_token_limit=650,
                human_prefix='Человек',
                ai_prefix='ИИ',
                prompt=PromptTemplate(
                    template=mistral_saiga["conversation_summary_prompt"],
                    input_variables=['summary', 'new_lines'],
                ),
                chat_memory=history,
                verbose=True,
            ),
        )
        self.conversation_sum_bufw.llm.verbose = True
