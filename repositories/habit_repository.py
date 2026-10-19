from datetime import date

from database.db import get_db_connection
from models.habit import Habit


def add_habit(chat_id: int, title: str) -> int:
    con = get_db_connection()

    try:
        cur = con.execute(
            """
            INSERT INTO habits (chat_id, title)
            VALUES (?, ?)
            """,
            (chat_id, title),
        )
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def get_habits(chat_id: int) -> list[Habit]:
    con = get_db_connection()

    try:
        rows = con.execute(
            """
            SELECT id, chat_id, title, active
            FROM habits
            WHERE chat_id = ? AND active = 1
            ORDER BY id
            """,
            (chat_id,),
        ).fetchall()

        return [
            Habit(
                id=row[0],
                chat_id=row[1],
                title=row[2],
                active=bool(row[3]),
            )
            for row in rows
        ]
    finally:
        con.close()


def complete_habit(habit_id: int, chat_id: int) -> bool:
    con = get_db_connection()

    try:
        habit = con.execute(
            """
            SELECT id FROM habits
            WHERE id = ? AND chat_id = ? AND active = 1
            """,
            (habit_id, chat_id),
        ).fetchone()

        if habit is None:
            return False

        try:
            con.execute(
                """
                INSERT INTO habit_completions
                    (habit_id, completed_date)
                VALUES (?, ?)
                """,
                (habit_id, date.today().isoformat()),
            )
            con.commit()
            return True
        except Exception as exc:
            con.rollback()

            # UNIQUE(habit_id, completed_date) не позволяет
            # отметить привычку дважды за один день.
            if "UNIQUE constraint failed" in str(exc):
                return False
            raise
    finally:
        con.close()