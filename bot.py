import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# Token ko Render ke Environment Variable se lena
TOKEN = os.getenv("BOT_TOKEN")

# /start command ka reply
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running on Render 🚀")

# Bot start karna
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
