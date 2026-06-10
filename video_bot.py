"""
Telegram Video Bot — Auto-Delete After 30 Seconds
==================================================

HOW IT WORKS:
  1. You post a picture in your channel
  2. Under the picture you put a link like: t.me/YourBot?start=video1
  3. Someone clicks the link → bot sends them the video privately
  4. After 30 seconds → bot deletes the video

YOUR LINKS WILL LOOK LIKE:
  t.me/YourBot?start=video1
  t.me/YourBot?start=video2
  t.me/YourBot?start=video3
  ... as many as you want

SETUP:
  1. pip install python-telegram-bot==20.*
  2. Fill in BOT_TOKEN and VIDEO_MAP below
  3. python video_bot.py
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SETTINGS — fill these in
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOT_TOKEN = "8915721290:AAGJUas-Cogmz67Z9LBNuH8JsDnKxsP6gRg"  # from @BotFather

# Add one line per video:
#   "link_key": "file_id"
# The link_key is what goes after ?start=
VIDEO_MAP = {
    "video1": "FILE_ID_FOR_VIDEO_1",
    "video2": "FILE_ID_FOR_VIDEO_2",
    "video3": "FILE_ID_FOR_VIDEO_3",
    # add more here...
}

DELETE_AFTER_SECONDS = 30

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def delete_later(bot, chat_id, message_id):
    await asyncio.sleep(DELETE_AFTER_SECONDS)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logging.info(f"Deleted message {message_id} from {chat_id}")
    except Exception as e:
        logging.warning(f"Could not delete: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload = context.args[0] if context.args else None
    chat_id = update.effective_chat.id
    user = update.effective_user

    logging.info(f"User @{user.username} (id:{user.id}) clicked: {payload}")

    file_id = VIDEO_MAP.get(payload) if payload else None

    if not file_id:
        await update.message.reply_text(
            "❌ This link is not valid. Please use a correct link from our channel."
        )
        return

    sent = await update.message.reply_video(
        video=file_id,
        caption=f"⏳ This video will be deleted in {DELETE_AFTER_SECONDS} seconds.",
        supports_streaming=True,
    )

    # delete after 30 seconds in background
    asyncio.create_task(
        delete_later(context.bot, chat_id, sent.message_id)
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logging.info("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
