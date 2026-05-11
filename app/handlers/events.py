from telegram import Update
from telegram.ext import ContextTypes

from app.services.events_service import format_events


async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = format_events()
    await update.message.reply_text(text)


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = format_events("buy")
    await update.message.reply_text(text)


async def booked_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = format_events("booked")
    await update.message.reply_text(text)