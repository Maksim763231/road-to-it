from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from repositories.habit_repository import (
    add_habit,
    get_habits,
    complete_habit,
)

router = Router()


@router.message(Command("habits"))
async def habits_handler(message: Message):
    habits = get_habits(message.chat.id)

    if not habits:
        await message.answer(
            "Пока привычек нет.\n"
            "Создай первую: /addhabit Читать 30 минут"
        )
        return

    text = "🎯 Твои привычки:\n\n"

    for habit in habits:
        text += f"{habit.id}. {habit.title}\n"

    text += "\nОтметить выполнение: /done ID"

    await message.answer(text)


@router.message(Command("addhabit"))
async def add_habit_handler(
    message: Message,
    command: CommandObject,
):
    title = (command.args or "").strip()

    if not title:
        await message.answer(
            "Укажи название.\n"
            "Пример: /addhabit Читать Python"
        )
        return

    habit_id = add_habit(message.chat.id, title)

    await message.answer(
        f"✅ Привычка добавлена!\n"
        f"ID: {habit_id}\n"
        f"Название: {title}"
    )


@router.message(Command("done"))
async def done_handler(
    message: Message,
    command: CommandObject,
):
    try:
        habit_id = int(command.args or "")
    except ValueError:
        await message.answer("Укажи ID, например: /done 1")
        return

    success = complete_habit(habit_id, message.chat.id)

    if success:
        await message.answer("✅ Привычка выполнена!")
    else:
        await message.answer(
            "Не удалось отметить привычку. "
            "Проверь ID или попробуй завтра."
        )