import datetime
import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection, Cursor

from config import settings


@dataclass
class DBService:
    conn: Connection
    cursor: Cursor

    def __init__(self):
        self.conn = sqlite3.connect(settings.DB_FILE)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS server_events
            (id INTEGER PRIMARY KEY AUTOINCREMENT, event_date TEXT)"""
        )
        self.conn.commit()

    def get_last_event_date(self) -> str:
        self.cursor.execute("SELECT MAX(event_date) FROM server_events")
        last_event_date = self.cursor.fetchone()[0]
        return last_event_date

    def insert_failure_event(self) -> None:
        self.cursor.execute("INSERT INTO server_events (event_date) VALUES (?)", (datetime.datetime.now(),))
        self.conn.commit()
