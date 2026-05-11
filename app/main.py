from telegram.ext import ApplicationBuilder, CommandHandler

from app.config import config
from app.database import init_db
from app.handlers.common import start_command, help_command
from app.handlers.events import events_command, buy_command, booked_command


def main():
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing. Check your .env file.")
    
    init_db()

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("events", events_command))
    app.add_handler(CommandHandler("buy", buy_command))
    app.add_handler(CommandHandler("booked", booked_command))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()