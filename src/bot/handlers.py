import asyncio

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from models.models import SaigaLLM
from src.bot.text_service import (
    collect_chat_history,
    drop_context,
    search_agent_service,
    show_chat_history,
    single_message_predict,
    text_chat_history,
    text_chat_service,
)


async def text_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = text_chat_service(
        update.effective_chat.id,
        update.message.from_user.id,
        update.message.text,
        update.message.date,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def text_chat_history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = text_chat_history(
        update.effective_chat.id,
        update.message.from_user.id,
        update.message.text,
        update.message.date,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def single_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = single_message_predict(
        update.effective_chat.id,
        update.message.from_user.id,
        update.message.text,
        update.message.date,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = search_agent_service(
        update.message.from_user.id, update.message.text, update.message.date
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def drop_context_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    drop_context(update.effective_chat.id)
    drop_context(update.message.from_user.id)
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


async def handle_store_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    collect_chat_history(
        update.effective_chat.id,
        update.message.from_user.id,
        update.message.text,
        update.message.date,
    )
    await asyncio.sleep(0)


async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = show_chat_history(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )
