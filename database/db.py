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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL,
            UNIQUE(habit_id, completed_date)
        )
    """)

    con.commit()
    con.close()
create_tables()
