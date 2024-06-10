import os
import sys
from typing import Sequence

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain.schema import BaseMessage
from loguru import logger

from src.models.conversation import BaseConversation
from src.models.models import BaseLLM


class LLMService:
    def __init__(self, llm: BaseLLM, conversation: BaseConversation):
        self.llm = llm
        self.conversation = conversation

    def generate_response_for_history(self, history: Sequence[BaseMessage]) -> str:
        for msg in history:
            if msg.type == "user":
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
