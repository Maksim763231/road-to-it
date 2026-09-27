import sqlite3

from sqlite3 import Connection


def get_db_connection() -> Connection:
    con = sqlite3.connect("database/bot.db")
    return con


def create_tables():
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            time TEXT,
            enabled BOOLEAN,
            timezone TEXT
        )
    """)

    con.commit()
    con.close()
create_tables()
