from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from models.models import SaigaLLM
from src.bot.text_service import (
    full_history_predict,
    single_message_predict,
    text_chat_service,
)
from src.data.utils import drop_context


async def text_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = text_chat_service(
        update.message.from_user.id, update.message.text, update.message.date
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def single_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = single_message_predict(
        update.message.from_user.id, update.message.text, update.message.date
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def full_history_predict_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    reply_msg = full_history_predict(
        update.message.from_user.id, update.message.text, update.message.date
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def drop_context_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    drop_context()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Context dropped!",
        reply_to_message_id=update.message.id,
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello!",
        reply_to_message_id=update.message.id,
    )


async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.from_user.id,
        reply_to_message_id=update.message.id,
    )
