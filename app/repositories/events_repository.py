import sqlite3
from typing import Any

from app.database import get_connection


def get_events_by_status(status: str | None = None) -> list[sqlite3.Row]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if status:
            cursor.execute(
                """
                SELECT *
                FROM events
                WHERE status = ?
                ORDER BY date_from ASC, start_time ASC
                """,
                (status,),
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
                event_type,
                date_from,
                date_to,
                start_time,
                url,
                price,
                status,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_data["title"],
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


def update_event_status_in_db(event_id: int, new_status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE events
            SET status = ?
            WHERE id = ?
            """,
            (new_status, event_id),
        )

        conn.commit()

        return cursor.rowcount > 0