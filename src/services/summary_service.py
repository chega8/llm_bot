from transformers import T5ForConditionalGeneration, T5Tokenizer

from src.data.history import PostgresHistory
from src.dep.postgres import get_postgres


class SummaryService:
    def __init__(self):
        model_name = 'utrobinmv/t5_summary_en_ru_zh_base_2048'
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)

    def summarize(self, text: str) -> str:
        prefix = 'summary: '
        src_text = prefix + text
        input_ids = self.tokenizer(
            src_text, max_length=512, truncation=True, return_tensors="pt"
        )

        generated_tokens = self.model.generate(
            **input_ids, min_length=80, max_length=100
        )

        result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return result[0]

    def summarize_history(self, history) -> str:
        text = "\n".join([f"{msg.content}" for msg in history.messages])
        return self.summarize(text)
