import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest

from src.dep.llm import get_saiga_llm_llamacpp
from src.models.conversation import DEFAULT_SYSTEM_PROMPT, SaigaConversation
from src.models.utils import *


@pytest.fixture
def llm():
    return get_saiga_llm_llamacpp(vocab_only=True)


@pytest.fixture
def conversation():
    return SaigaConversation()


def test_prompt_size(llm, conversation):
    print(len(DEFAULT_SYSTEM_PROMPT))
    print(llm.get_num_tokens(DEFAULT_SYSTEM_PROMPT))
    print(llm.get_num_tokens(conversation.get_prompt()))

    msg = "Hello, how are you, tell me a joke about liberals"
    print(len(msg))
    conversation.add_user_message(msg)
    print(llm.get_num_tokens(msg))
    print(llm.get_num_tokens(conversation.get_prompt()))
