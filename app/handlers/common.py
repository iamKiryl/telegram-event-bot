from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для событий и концертов.\n\n"
        "Команды:\n"
        "/events — список событий\n"
        "/buy — хочу купить\n"
        "/booked — уже забронировано\n"
        "/help — помощь"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — старт\n"
        "/help — помощь\n"
        "/events — показать события\n"
        "/buy — события со статусом buy\n"
        "/booked — события со статусом booked"
    )