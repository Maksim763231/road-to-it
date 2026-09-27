from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from models.user import User
from repositories.user_repository import save_user, get_user

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    user = get_user(message.chat.id)
    if not user:
        user = User(
            chat_id=message.chat.id,
            username=message.from_user.username,
            time="08:00",
            enabled=True,
            timezone="Europe/Moscow"
        )
        save_user(user)

    await message.answer("Привет! Я твой личный Telegram-бот 🚀")
