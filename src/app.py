import os
import random
import sys
from pathlib import Path

from loguru import logger
from prometheus_client import Counter
from telegram import Bot, StickerSet, Update
from telegram.ext import CallbackContext, Updater

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from telegram import Update
from telegram.ext import (
    Application,
    BaseHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.bot.handlers import *
from src.conf import settings


def main() -> None:
    Path(".tmp").mkdir(parents=True, exist_ok=True)

    app = Application.builder().token(settings.bot.token).build()

    app.add_handlers(
        [
            CommandHandler("start", handle_start, block=False),
            CommandHandler("my_id", handle_user_id, block=False),
            CommandHandler("msg", single_message_handler, block=False),
            CommandHandler("chat", text_chat_history_handler, block=False),
            CommandHandler("drop", drop_context_handler, block=False),
            CommandHandler("agent", search_handler, block=False),
            CommandHandler("show", show_history, block=False),
            CommandHandler("summary", show_history_summary, block=False),
            CommandHandler("tox", tox, block=False),
            MessageHandler(filters.TEXT, handle_store_msg, block=False),
        ]
    )
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        errors_counter = Counter(
            'application_errors', 'Number of errors in the application'
        )
        main()
    except Exception as ex:
        logger.error(ex)
        errors_counter.inc()
