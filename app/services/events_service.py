from app.repositories.events_repository import get_events_by_status


def format_events(status: str | None = None) -> str:
    events = get_events_by_status(status)

    if not events:
        if status:
            return f"Событий со статусом '{status}' пока нет."
        return "Событий пока нет."

    lines = []

    for event in events:
        lines.append(
            f"#{event['id']} — {event['title']}\n"
            f"Тип: {event['event_type']}\n"
            f"Дата: {event['date_from'] or '-'} {event['start_time'] or ''}\n"
            f"Цена: {event['price'] or '-'}\n"
            f"Статус: {event['status']}\n"
            f"Ссылка: {event['url'] or '-'}\n"
        )

    return "\n".join(lines)