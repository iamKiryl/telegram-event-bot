from telegram.ext import ApplicationBuilder, CommandHandler

from app.config import config
from app.database import init_db


async def start_command(update, context):
    await update.message.reply_text(
        "Привет! Я бот для событий и концертов.\n\n"
        "Команды:\n"
        "/events — список событий\n"
        "/buy — хочу купить\n"
        "/booked — уже забронировано\n"
        "/help — помощь"
    )


async def help_command(update, context):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — старт\n"
        "/help — помощь\n"
        "/events — показать события\n"
        "/buy — события со статусом buy\n"
        "/booked — события со статусом booked"
    )


def main():
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing. Check your .env file.")
    
    init_db()

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()