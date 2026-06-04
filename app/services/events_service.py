from app.repositories.events_repository import (
    get_event_by_id,
    get_events_by_status,
    insert_event,
    update_event_status_in_db,
)


VALID_STATUSES = {
    "wishlist",
    "buy",
    "booked",
    "done",
    "skipped",
    "cancelled",
}


def normalize_optional(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()

    if not value or value == "-":
        return None

    return value


def parse_price(value: str | None) -> float | None:
    value = normalize_optional(value)
    print(f"Parsing price from '{value}'")
    if value is None:
        return None

    value = value.replace("PLN", "").replace("zł", "").replace(" ", "")
    value = value.replace(",", ".")

    try:
        return float(value)
    except ValueError:
        raise ValueError("Цена должна быть числом.")


def format_price(price: float | None) -> str:
    if price is None:
        return "-"

    return f"{price:g} PLN"


def format_events(status: str | None = None) -> str:
    events = get_events_by_status(status)

    if not events:
        if status:
            return f"Событий со статусом '{status}' пока нет."
        return "Событий пока нет."

    lines = ["События:\n"]

    for event in events:
        lines.append(
            f"#{event['id']} — {event['title']}\n"
            f"Тип: {event['event_type']}\n"
            f"Дата: {event['date_from'] or '-'} {event['start_time'] or ''}\n"
            f"Цена: {format_price(event['price'])}\n"
            f"Статус: {event['status']}\n"
            f"Ссылка: {event['url'] or '-'}\n"
        )

    return "\n".join(lines)


def update_event_status(event_id: int, new_status: str) -> dict:
    new_status = new_status.strip().lower()

    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Недопустимый статус '{new_status}'. "
            f"Допустимые значения: {', '.join(sorted(VALID_STATUSES))}"
        )

    updated = update_event_status_in_db(event_id, new_status)

    if not updated:
        raise LookupError(f"Событие с ID {event_id} не найдено.")

    return {
        "event_id": event_id,
        "new_status": new_status,
        "success": True,
    }


def add_event(
    title: str,
    telegram_user_id: int,
    event_type: str = "concert",
    date_from: str | None = None,
    date_to: str | None = None,
    start_time: str | None = None,
    url: str | None = None,
    price: float | None = None,
    status: str = "wishlist",
    notes: str | None = None,
) -> dict:
    title = title.strip()
    event_type = event_type.strip() if event_type else "concert"
    status = status.strip().lower()

    if not title:
        raise ValueError("Название события не может быть пустым.")

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Недопустимый статус '{status}'. "
            f"Допустимые значения: {', '.join(sorted(VALID_STATUSES))}"
        )

    if price is not None and price < 0:
        raise ValueError("Цена не может быть отрицательной.")

    event_data = {
        "title": title,
        "event_type": event_type,
        "date_from": normalize_optional(date_from),
        "date_to": normalize_optional(date_to),
        "start_time": normalize_optional(start_time),
        "url": normalize_optional(url),
        "price": price,
        "status": status,
        "notes": normalize_optional(notes),
        "telegram_user_id": telegram_user_id,
    }

    new_id = insert_event(event_data)

    return {"id": new_id, **event_data}

def update_event_status(
    telegram_user_id: int,
    event_id: int,
    new_status: str,
) -> dict:
    new_status = new_status.strip().lower()

    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Недопустимый статус '{new_status}'. "
            f"Допустимые значения: {', '.join(sorted(VALID_STATUSES))}"
        )

    event = get_event_by_id(telegram_user_id, event_id)

    if event is None:
        raise LookupError("Событие не найдено.")

    updated = update_event_status_in_db(
        telegram_user_id=telegram_user_id,
        event_id=event_id,
        new_status=new_status,
    )

    if not updated:
        raise LookupError("Не удалось обновить событие.")

    return {
        "event_id": event_id,
        "title": event["title"],
        "new_status": new_status,
        "success": True,
    }

def add_event_from_text(text: str, telegram_user_id: int) -> str:
    parts = [part.strip() for part in text.split("|")]

    if len(parts) < 2:
        return (
            "Неверный формат.\n\n"
            "Используй:\n"
            "/add Название | дата | время | цена | ссылка | статус | заметки\n\n"
            "Пример:\n"
            "/add Linkin Park | 2026-06-10 | 20:00 | 250 | https://example.com | wishlist | хочу сходить"
        )

    while len(parts) < 7:
        parts.append("")

    title, date_from, start_time, price_raw, url, status, notes = parts[:7]

    price = parse_price(price_raw)

    event = add_event(
        title=title,
        event_type="concert",
        date_from=date_from,
        date_to=None,
        start_time=start_time,
        url=url,
        price=price,
        status=status or "wishlist",
        notes=notes,
        telegram_user_id=telegram_user_id,
    )

    return (
        "Событие добавлено:\n\n"
        f"#{event['id']} — {event['title']}\n"
        f"Дата: {event['date_from'] or '-'} {event['start_time'] or ''}\n"
        f"Цена: {format_price(event['price'])}\n"
        f"Статус: {event['status']}\n"
        f"Ссылка: {event['url'] or '-'}\n"
        f"Заметки: {event['notes'] or '-'}"
    )