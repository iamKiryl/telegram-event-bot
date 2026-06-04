from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    await update.message.reply_text(
        "Привет! Я бот для событий и концертов.\n\n"
        "Команды:\n"
        "/events — список событий\n"
        "/buy — события со статусом buy\n"
        "/booked — события со статусом booked\n"
        "/add — добавить событие\n"
        "/status — изменить статус события\n"
        "/help — помощь"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    await update.message.reply_text(
        "Доступные команды:\n\n"
        "/start — старт\n"
        "/help — помощь\n"
        "/events — показать все события\n"
        "/buy — показать события со статусом buy\n"
        "/booked — показать события со статусом booked\n"
        "/add — добавить событие\n"
        "/status — изменить статус события через кнопки\n\n"
        "Добавить событие:\n"
        "/add Название | дата | время | цена | ссылка | статус | заметки\n\n"
        "Пример:\n"
        "/add Linkin Park | 2026-06-10 | 20:00 | 250 | https://example.com | wishlist | хочу сходить\n\n"
        "Статусы:\n"
        "wishlist, buy, booked, done, skipped, cancelled"
    )