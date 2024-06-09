import os
import random
import sys
from pathlib import Path

from loguru import logger
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
from src.models import SaigaLLM


def main() -> None:
    Path(".tmp").mkdir(parents=True, exist_ok=True)

    app = Application.builder().token(settings.telegram.token).build()

    app.add_handlers(
        [
            CommandHandler("start", handle_start, block=False),
            CommandHandler("my_id", handle_user_id, block=False),
            CommandHandler("msg", single_message_handler, block=False),
            CommandHandler("ctx", text_chat_handler, block=False),
            CommandHandler("hist", full_history_predict_handler, block=False),
            CommandHandler("drop", drop_context_handler, block=False),
            MessageHandler(filters.TEXT, text_chat_handler, block=False),
        ]
    )
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    # try:
    #     main()
    # except Exception as ex:
    #     logger.error(ex)
