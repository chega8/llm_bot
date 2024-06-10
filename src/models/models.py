from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

from src.conf import settings
from src.dep.llm import get_saiga_llm_llamacpp


class BaseLLM:
    def __init__(self) -> None:
        self.llm = None

    def predict_raw_prompt(self, prompt: str) -> str:
        ...


class SaigaLLM(BaseLLM):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.llm = get_saiga_llm_llamacpp()

    def predict(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
