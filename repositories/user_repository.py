from database.db import get_db_connection
from models.user import User


def save_user(user: User):
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO users (
            chat_id,
            username,
            time,
            enabled,
            timezone
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user.chat_id,
        user.username,
        user.time,
        user.enabled,
        user.timezone
    ))

    con.commit()
    con.close()

def get_user(chat_id: int) -> User | None:
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT chat_id, username, time, enabled, timezone
        FROM users
        WHERE chat_id = ?
    """, (chat_id,))

    row = cur.fetchone()

    con.close()

    if row is None:
        return None

    return User(
        chat_id=row[0],
        username=row[1],
        time=row[2],
        enabled=bool(row[3]),
        timezone=row[4]
    )

def get_all_users() -> list[User]:
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT chat_id, username, time, enabled, timezone
        FROM users
    """)

    rows = cur.fetchall()

    con.close()

    return [
        User(
            chat_id=row[0],
            username=row[1],
            time=row[2],
            enabled=bool(row[3]),
            timezone=row[4]
        )
        for row in rows
    ]
get_all_users()