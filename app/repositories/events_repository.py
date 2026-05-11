import sqlite3
from app.database import get_connection


def get_events_by_status(status: str | None = None):
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