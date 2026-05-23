from telegram import Update
from telegram.ext import ContextTypes

from app.services.events_service import (
    add_event_from_text,
    format_events,
    update_event_status_from_text,
)


async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = format_events()
    await update.message.reply_text(text)


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = format_events("buy")
    await update.message.reply_text(text)


async def booked_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = format_events("booked")
    await update.message.reply_text(text)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    payload = (update.message.text or "").removeprefix("/add").strip()

    try:
        result = add_event_from_text(payload)
    except ValueError as error:
        result = str(error)

    await update.message.reply_text(result)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    payload = (update.message.text or "").removeprefix("/status").strip()

    try:
        result = update_event_status_from_text(payload)
    except ValueError as error:
        result = str(error)
    except LookupError as error:
        result = str(error)

    await update.message.reply_text(result)