import sqlite3
from typing import Any

from app.database import get_connection


def get_events_by_status(
        telegram_user_id: int,
        status: str | None = None
        ) -> list[sqlite3.Row]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if status:
            cursor.execute(
                """
                SELECT *
                FROM events
                WHERE telegram_user_id = ? AND status = ?
                ORDER BY date_from ASC, start_time ASC
                """,
                (telegram_user_id, status),
            )
        else:
            cursor.execute(
                """
                SELECT *
                FROM events
                ORDER BY date_from ASC, start_time ASC
                """
            )

        return cursor.fetchall()


def insert_event(event_data: dict[str, Any]) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO events (
                title,
                telegram_user_id,
                event_type,
                date_from,
                date_to,
                start_time,
                url,
                price,
                status,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_data["title"],
                event_data["telegram_user_id"],
                event_data["event_type"],
                event_data["date_from"],
                event_data["date_to"],
                event_data["start_time"],
                event_data["url"],
                event_data["price"],
                event_data["status"],
                event_data["notes"],
            ),
        )

        conn.commit()

        return cursor.lastrowid


def update_event_status_in_db(
    telegram_user_id: int,
    event_id: int,
    new_status: str,
) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE events
            SET status = ?
            WHERE id = ?
              AND telegram_user_id = ?
            """,
            (new_status, event_id, telegram_user_id),
        )

        conn.commit()

        return cursor.rowcount > 0
    
def get_event_by_id(
    telegram_user_id: int,
    event_id: int,
) -> sqlite3.Row | None:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM events
            WHERE id = ?
              AND telegram_user_id = ?
            """,
            (event_id, telegram_user_id),
        )

        return cursor.fetchone()
    
def get_event_by_position(
    telegram_user_id: int,
    position: int,
    status: str | None = None,
) -> sqlite3.Row | None:
    events = get_events_by_status(telegram_user_id, status)

    index = position - 1

    if index < 0 or index >= len(events):
        return None

    return events[index]

def update_user_event_status_in_db(
    telegram_user_id: int,
    position: int,
    new_status: str,
) -> bool:
    event = get_event_by_position(telegram_user_id, position)

    if event is None:
        return False

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE events
            SET status = ?
            WHERE id = ?
              AND telegram_user_id = ?
            """,
            (new_status, event["id"], telegram_user_id),
        )

        conn.commit()
        return cursor.rowcount > 0
