import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8915721290:AAGJUas-Cogmz67Z9LBNuH8JsDnKxsP6gRg"

# ============================================
# ADD OR REMOVE CHANNELS HERE
# Format: "Channel Name": "@username"
# ============================================
CHANNELS = {
    "Channel 1": "@haparotV",
}

# ============================================
# ADD YOUR VIDEOS HERE
# Format: "linkname": "file_id"
# ============================================
VIDEO_MAP = {
    "video1": "FILE_ID_FOR_VIDEO_1",
    "video2": "FILE_ID_FOR_VIDEO_2",
}

async def check_subscriptions(user_id, bot):
    not_joined = []
    for name, username in CHANNELS.items():
        try:
            member = await bot.get_chat_member(chat_id=username, user_id=user_id)
            if member.status in ["left", "banned", "kicked"]:
                not_joined.append((name, username))
        except:
            not_joined.append((name, username))
    return not_joined

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Please use a special link to get a video.")
        return

    payload = args[0]
    context.user_data["payload"] = payload

    not_joined = await check_subscriptions(update.effective_user.id, context.bot)

    if not_joined:
        buttons = [[InlineKeyboardButton(name, url=f"https://t.me/{username.strip('@')}")] for name, username in not_joined]
        buttons.append([InlineKeyboardButton("✅ I Subscribed", callback_data=f"check_{payload}")])
        markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            "⚠️ To receive this video, please subscribe to these channels first:",
            reply_markup=markup
        )
        return

    await send_video(update.message, context, payload)

async def button_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    payload = query.data.replace("check_", "")
    not_joined = await check_subscriptions(query.from_user.id, context.bot)

    if not_joined:
        buttons = [[InlineKeyboardButton(name, url=f"https://t.me/{username.strip('@')}")] for name, username in not_joined]
        buttons.append([InlineKeyboardButton("✅ I Subscribed", callback_data=f"check_{payload}")])
        markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            "❌ You still haven't subscribed to all channels. Please subscribe first:",
            reply_markup=markup
        )
        return

    await query.edit_message_text("✅ Verified! Sending your video...")
    await send_video(query.message, context, payload)

async def send_video(message, context, payload):
    video_id = VIDEO_MAP.get(payload)
    if not video_id:
        await message.reply_text("Invalid link.")
        return
    msg = await message.reply_video(video=video_id)
    await asyncio.sleep(30)
    await context.bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.video.file_id
    await update.message.reply_text(f"Your file_id:\n`{file_id}`", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_check))
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.VIDEO, get_file_id))
    print("Bot is running...")
    app.run_polling()
