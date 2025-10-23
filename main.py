from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import asyncio

BOT_TOKEN = "token_here" #your bot token, get it on @botfather
OWNER_ID = 1234 #your telegram id, get it on @WhatChatIDBot
map_ids = {}

FAQ_TEXT = """FaQ, you can change it how you need
""" #faq text

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        return
    await update.message.reply_text(FAQ_TEXT)

async def user_message(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        return
    if update.message.text and update.message.text.startswith("/"):
        return
    fwd = await context.bot.forward_message(chat_id=OWNER_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    map_ids[fwd.message_id] = update.effective_chat.id

async def owner_message(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if not update.message.reply_to_message:
        return
    replied = update.message.reply_to_message.message_id
    if replied not in map_ids:
        return
    target = map_ids[replied]
    await context.bot.copy_message(chat_id=target, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.User(OWNER_ID), user_message))
    app.add_handler(MessageHandler(filters.User(OWNER_ID) & filters.ALL, owner_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())