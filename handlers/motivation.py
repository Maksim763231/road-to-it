from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from quotes import get_random_quote

router = Router()

quote_button = InlineKeyboardButton(
    text = "🔄 Ещё цитату",
    callback_data = "new_quote"
)
quote_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [[quote_button]]
)
def format_quote(quote):
    return (
        f"🌅 Цитата дня\n\n"
        f"«{quote}»\n\n"
        f"🚀 Хорошего дня!"
    )

@router.message(Command("quote"))
async def quote_handler(message: Message):
    quote = get_random_quote()
    text = format_quote(quote)
    await message.answer(
        text,
        reply_markup = quote_keyboard
    )

@router.callback_query(lambda callback: callback.data == "new_quote")
async def new_quote_handler(callback: CallbackQuery):
    quote = get_random_quote()
    text = format_quote(quote)
    await callback.answer()
    await callback.message.edit_text(
        text,
        reply_markup = quote_keyboard
    )
