import os
import sys
from shutil import rmtree

from loguru import logger

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from src.data.history import FileChatMessageHistory


def merge_all_files():

    all_users = os.listdir("data/history")
    full_messages = []
    for user in all_users:
        history = FileChatMessageHistory("data/history", int(user.replace(".json", "")))
        messages = history.messages[1:]
        full_messages.extend([msg.content.replace("\n", "") for msg in messages])

    logger.info(f"Total messages: {len(full_messages)}")
    logger.info(f"Total users: {len(all_users)}")
    return full_messages


def drop_context():
    pth = "data/history"
    rmtree(pth)
