from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

from app.config import config
from app.database import init_db
from app.handlers.common import help_command, start_command
from app.handlers.events import (
    add_command,
    booked_command,
    buy_command,
    delete_cancel_callback,
    delete_command,
    delete_confirm_callback,
    delete_event_callback,
    events_command,
    status_command,
    status_event_callback,
    status_set_callback,
)


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
    app.add_handler(CommandHandler("add", add_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("delete", delete_command))

    app.add_handler(CallbackQueryHandler(status_event_callback, pattern="^status_event:"))
    app.add_handler(CallbackQueryHandler(status_set_callback, pattern="^status_set:"))
    app.add_handler(CallbackQueryHandler(delete_event_callback, pattern="^delete_event:"))
    app.add_handler(CallbackQueryHandler(delete_confirm_callback, pattern="^delete_confirm:"))
    app.add_handler(CallbackQueryHandler(delete_cancel_callback, pattern="^delete_cancel:"))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()