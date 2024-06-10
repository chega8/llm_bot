# <|im_start|>system
# You are MistralOrca, a large language model trained by Alignment Lab AI. Write out your reasoning step-by-step to be sure you get the right answers!
# <|im_end|>
# <|im_start|>user
# How are you?<|im_end|>
# <|im_start|>assistant
# I am doing well!<|im_end|>
# <|im_start|>user
# Please tell me about how mistral winds have attracted super-orcas.<|im_end|>
# <|im_start|>assistant


def convert_prompt(text):
    sys_prompt = "You are MistralOrca, a large language model trained by Alignment Lab AI. Write out your reasoning step-by-step to be sure you get the right answers!"
    msg_template = "<|im_start|>{role}\n{content}<|im_end|>\n"
    response_template = "<|im_start|>assistant\n"

    messages = [msg_template.format(role="system", content=sys_prompt)]
    messages.append(msg_template.format(role="user", content=text))
    messages.append(response_template)

    messages = [{"role": "system", "content": sys_prompt}]
    messages.append({"role": "user", "content": text})

    final_text = ""
    for message in messages:
        message_text = msg_template.format(**message)
        final_text += message_text
    final_text += response_template
    return final_text.strip()


print(convert_prompt("How are you?"))
