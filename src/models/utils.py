from typing import Sequence

from langchain.schema import BaseMessage
from langchain_community.llms import LlamaCpp


def cut_prompt(
    prompt: str,
    llm,
    tokens_in_prompt: int,
    max_tokens: int = 1024,
    tokens_to_generate: int = 512,
) -> str:
    num_tokens = llm.get_num_tokens(prompt)
    tail = max_tokens - num_tokens
    # tokens_to_cut = num_tokens - keep_tokens + tokens_to_generate - tail + 1
    tokens_to_cut = max_tokens - tokens_to_generate - tokens_in_prompt

    symbols_to_cut = tokens_to_cut * 2.5
    return prompt[-symbols_to_cut:]
