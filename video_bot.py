import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

VIDEO_MAP = {
    "video1": "FILE_ID_FOR_VIDEO_1",
    "video2": "FILE_ID_FOR_VIDEO_2",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Please use a special link to get a video.")
        return

    payload = arg
