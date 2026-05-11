import sqlite3
from app.config import config


def get_connection():
    return sqlite3.connect(config.DATABASE_PATH)


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                event_type TEXT NOT NULL DEFAULT 'concert',
                date_from TEXT,
                date_to TEXT,
                start_time TEXT,
                url TEXT,
                price REAL,
                status TEXT NOT NULL DEFAULT 'wishlist',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()