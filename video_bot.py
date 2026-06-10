import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8915721290:AAGJUas-Cogmz67Z9LBNuH8JsDnKxsP6gRg"

VIDEO_MAP = {
    "video1": "FILE_ID_FOR_VIDEO_1",
    "video2": "FILE_ID_FOR_VIDEO_2",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Please use a special link to get a video.")
        return
    payload = args[0]
    video_id = VIDEO_MAP.get(payload)
    if not video_id:
        await update.message.reply_text("Invalid link.")
        return
    msg = await update.message.reply_video(video=video_id)
    await asyncio.sleep(30)
    await context.bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
