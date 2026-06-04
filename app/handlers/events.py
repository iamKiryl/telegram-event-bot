from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.events_service import (
    add_event_from_text,
    format_events,
    update_event_status,
)

from app.repositories.events_repository import get_events_by_status
from app.services.events_service import VALID_STATUSES


async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    telegram_user_id = update.effective_user.id

    text = format_events(telegram_user_id)
    await update.message.reply_text(text)


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    telegram_user_id = update.effective_user.id
    text = format_events(telegram_user_id, "buy")
    await update.message.reply_text(text)


async def booked_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    telegram_user_id = update.effective_user.id
    text = format_events(telegram_user_id, "booked")
    await update.message.reply_text(text)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    payload = (update.message.text or "").removeprefix("/add").strip()
    try:
        telegram_user_id = update.effective_user.id
        result = add_event_from_text(payload, telegram_user_id)
    except ValueError as error:
        result = str(error)

    await update.message.reply_text(result)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    telegram_user_id = update.effective_user.id
    events = get_events_by_status(telegram_user_id)

    if not events:
        await update.message.reply_text("У тебя пока нет событий.")
        return

    keyboard = []

    for event in events:
        title = event["title"]
        current_status = event["status"]

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{title} — {current_status}",
                    callback_data=f"status_event:{event['id']}",
                )
            ]
        )

    await update.message.reply_text(
        "Выбери событие, которому хочешь изменить статус:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def status_event_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query or not query.from_user:
        return

    await query.answer()

    telegram_user_id = query.from_user.id
    data = query.data or ""

    event_id_raw = data.removeprefix("status_event:")

    try:
        event_id = int(event_id_raw)
    except ValueError:
        await query.edit_message_text("Некорректное событие.")
        return

    keyboard = []

    for status in sorted(VALID_STATUSES):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=status,
                    callback_data=f"status_set:{event_id}:{status}",
                )
            ]
        )

    await query.edit_message_text(
        "Теперь выбери новый статус:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def status_set_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query or not query.from_user:
        return

    await query.answer()

    telegram_user_id = query.from_user.id
    data = query.data or ""

    try:
        _, event_id_raw, new_status = data.split(":")
        event_id = int(event_id_raw)
    except ValueError:
        await query.edit_message_text("Некорректные данные.")
        return

    try:
        result = update_event_status(
            telegram_user_id=telegram_user_id,
            event_id=event_id,
            new_status=new_status,
        )
    except ValueError as error:
        await query.edit_message_text(str(error))
        return
    except LookupError as error:
        await query.edit_message_text(str(error))
        return

    await query.edit_message_text(
        "Статус обновлён:\n\n"
        f"{result['title']}\n"
        f"Новый статус: {result['new_status']}"
    )