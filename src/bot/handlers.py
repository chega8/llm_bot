import asyncio
import random

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from src.services.text_bot_service import TextSerivce, TextSerivcev2

text_bot_service = TextSerivce()


# text_bot_service2 = TextSerivcev2()


async def text_chat_history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = text_bot_service.text_chat_history(
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
    reply_msg = text_bot_service.single_message_predict(
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
    reply_msg = text_bot_service.search_agent_service(
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


async def drop_context_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_bot_service.drop_context(
        update.effective_chat.id,
        update.message.from_user.id,
        update.message.text,
        update.message.date,
    )
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
    text_bot_service.collect_chat_history(
        update.effective_chat.id,
        update.message.from_user.id,
        update.message.text,
        update.message.date,
    )

    txt = update.message.text

    if len(txt.split()) > 1 and random.random() < 0.05:
        reply_msg = text_bot_service.toxic_predict(txt)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_msg,
            reply_to_message_id=update.message.id,
        )

    await asyncio.sleep(0)


async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = text_bot_service.show_chat_history(
        update.effective_chat.id,
        update.message.from_user.id,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def show_history_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg = text_bot_service.history_summary(
        update.effective_chat.id, update.message.from_user.id
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )


async def tox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text

    reply_msg = text_bot_service.toxic_predict(txt)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg,
        reply_to_message_id=update.message.id,
    )
