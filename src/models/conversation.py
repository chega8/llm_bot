from loguru import logger

from data.prompts import CONVERSATION_PROMPT, DEFAULT_SYSTEM_PROMPT, SUMMARY_PROMPT


class BaseConversation:
    def __init__(
        self, system_prompt: str, message_template: str, response_template: str
    ):
        self.system_prompt = system_prompt
        self.message_template = message_template
        self.response_template = response_template
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_user_message(self, message):
        ...

    def add_bot_message(self, message):
        ...

    def get_prompt(self):
        ...


class SaigaConversation(BaseConversation):
    def __init__(
        self,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        message_template="<s>{role}\n{content}</s>",
        response_template="<s>bot\n",
    ):
        super().__init__(system_prompt, message_template, response_template)

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_bot_message(self, message):
        self.messages.append({"role": "bot", "content": message})

    def get_prompt(self):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += self.response_template
        return final_text.strip()


class DummyConversation(BaseConversation):
    def __init__(
        self,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        message_template="{role}\n{content}",
        response_template="ai\n",
    ):
        super().__init__(system_prompt, message_template, response_template)

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_bot_message(self, message):
        self.messages.append({"role": "bot", "content": message})

    def clear_messages(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def get_prompt(self, new_only=False):
        final_text = ""
        messages = self.messages if not new_only else self.messages[1:]
        for message in messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += self.response_template

        return final_text.strip()


class MistralConversation(BaseConversation):
    def __init__(
        self,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        message_template="<|im_start|>{role}\n{content}<|im_end|>\n",
        response_template="<|im_start|>assistant\n",
    ):
        super().__init__(system_prompt, message_template, response_template)

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_bot_message(self, message):
        self.messages.append({"role": "assistant", "content": message})

    def get_prompt(self):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += self.response_template

        # logger.info(f"final_text: {final_text}")
        return final_text.strip()
