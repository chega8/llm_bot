from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

from src.conf import settings


def get_saiga_llm_llamacpp(vocab_only=False):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=settings.model.path,
        temperature=settings.model.temperature,
        max_tokens=settings.model.max_tokens,
        n_ctx=settings.model.ctx,
        # n_gpu_layers=-1,  # for gpu
        callback_manager=callback_manager,
        verbose=False,
        vocab_only=vocab_only,
        echo=True,
    )
    return llm
