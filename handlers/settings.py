import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from services.scheduler import schedule_user
from repositories.user_repository import get_user, save_user

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
                    callback_data="settings:toggle",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏰ Изменить время",
                    callback_data="settings:time",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌍 Изменить часовой пояс",
                    callback_data="settings:timezone",
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
        reply_markup=get_settings_keyboard(user.enabled),
    )


@router.callback_query(lambda c: c.data == "settings:toggle")
async def toggle_motivation_handler(callback: CallbackQuery):
    user = get_user(callback.message.chat.id)

    if user is None:
        await callback.answer("Сначала отправь /start.", show_alert=True)
        return

    user.enabled = not user.enabled
    save_user(user)
    schedule_user(callback.bot, user)

    await callback.message.edit_text(
        format_settings(user),
        reply_markup=get_settings_keyboard(user.enabled),
    )
    await callback.answer("Настройки сохранены")


@router.callback_query(lambda c: c.data == "settings:time")
async def time_button_handler(callback: CallbackQuery):
    await callback.message.answer(
        "⏰ Отправь команду, например:\n/settime 09:30"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "settings:timezone")
async def timezone_button_handler(callback: CallbackQuery):
    await callback.message.answer(
        "🌍 Отправь команду, например:\n"
        "/settimezone Europe/Amsterdam"
    )
    await callback.answer()


@router.message(Command("settime"))
async def set_time_handler(
    message: Message,
    command: CommandObject,
):
    value = (command.args or "").strip()

    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
        await message.answer(
            "Неверный формат. Пример: /settime 09:30"
        )
        return

    user = get_user(message.chat.id)

    if user is None:
        await message.answer("Сначала отправь /start.")
        return

    user.time = value
    save_user(user)
    schedule_user(message.bot, user)

    await message.answer(f"⏰ Новое время: {user.time}")


@router.message(Command("settimezone"))
async def set_timezone_handler(
    message: Message,
    command: CommandObject,
):
    timezone_name = (command.args or "").strip()

    if not timezone_name:
        await message.answer(
            "Пример: /settimezone Europe/Amsterdam"
        )
        return

    try:
        ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError):
        await message.answer(
            "Неизвестный часовой пояс. "
            "Пример: Europe/Amsterdam"
        )
        return

    user = get_user(message.chat.id)

    if user is None:
        await message.answer("Сначала отправь /start.")
        return

    user.timezone = timezone_name
    save_user(user)
    schedule_user(message.bot, user)

    await message.answer(
        f"🌍 Новый часовой пояс: {user.timezone}"
    )