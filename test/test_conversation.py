import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_core.prompts.prompt import PromptTemplate

from data.prompts import CONVERSATION_PROMPT, SUMMARY_PROMPT
from src.data.history import FileChatMessageHistory
from src.dep.llm import get_saiga_llm_llamacpp


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.invoke(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result


def test_buffer_memory():
    llm = get_saiga_llm_llamacpp()
    history = FileChatMessageHistory('test/data/history', 228)

    conversation_sum_bufw = ConversationChain(
        llm=llm,
        prompt=PromptTemplate(
            template=CONVERSATION_PROMPT, input_variables=['history', 'input']
        ),
        memory=ConversationSummaryBufferMemory(
            llm=llm,
            max_token_limit=650,
            human_prefix='Человек',
            ai_prefix='ИИ',
            prompt=PromptTemplate(
                template=SUMMARY_PROMPT, input_variables=['summary', 'new_lines']
            ),
            chat_memory=history,
        ),
    )

    print('**** Buffer:')
    print(conversation_sum_bufw.memory.buffer)

    conversation_sum_bufw.invoke(
        "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
    )
    conversation_sum_bufw.invoke("Расскажи анекдот про либералов")
    conversation_sum_bufw.invoke("И какой из этого вывод?.")
    conversation_sum_bufw.invoke(
        "Не понял анекдот, можешь пояснить шаг за шагом, в чем смысл?"
    )

    print('**** Buffer:')
    print(conversation_sum_bufw.memory.buffer)


print(test_buffer_memory())
