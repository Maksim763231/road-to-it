from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.types import CallbackQuery

from repositories.user_repository import save_user
from repositories.user_repository import get_user

router = Router()

def get_settings_keyboard(enabled: bool) -> InlineKeyboardMarkup:
    toggle_text = (
        "🔕 Выключить мотивацию"
        if enabled
        else "🔔 Включить мотивацию"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=toggle_text,
                    callback_data="settings:toggle"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏰ Изменить время",
                    callback_data="settings:time"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌍 Изменить часовой пояс",
                    callback_data="settings:timezone"
                )
            ],
        ]
    )


def format_settings(user) -> str:
    status = "включена" if user.enabled else "выключена"

    return (
        "⚙️ Твои настройки\n\n"
        f"🔔 Мотивация: {status}\n"
        f"⏰ Время: {user.time}\n"
        f"🌍 Часовой пояс: {user.timezone}"
    )


@router.message(Command("settings"))
async def settings_handler(message: Message):
    user = get_user(message.chat.id)

    if user is None:
        await message.answer("Сначала отправь /start.")
        return

    await message.answer(
        format_settings(user),
        reply_markup=get_settings_keyboard(user.enabled)
    )

@router.callback_query(lambda c: c.data == "settings:toggle")
async def toggle_motivation_handler(callback: CallbackQuery):
    user = get_user(callback.message.chat.id)

    if user is None:
        await callback.message.answer("Сначала отправь /start.")
        return

    user.enabled = not user.enabled
    save_user(user)

    await callback.message.edit_text(
        format_settings(user),
        reply_markup=get_settings_keyboard(user.enabled)
    )
    await callback.answer("Настройки обновлены.")