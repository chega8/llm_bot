from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

from src.conf import settings


def get_saiga_llm_llamacpp():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=settings.model.path,
        temperature=settings.model.temperature,
        max_tokens=settings.model.max_tokens,
        n_ctx=settings.model.ctx,
        n_gpu_layers=-1,  # for gpu
        top_p=5,
        callback_manager=callback_manager,
        verbose=True,
    )
    return llm
