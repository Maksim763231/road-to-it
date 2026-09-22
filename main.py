import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from quotes import quotes
from quotes import get_random_quote

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
print(TOKEN is not None)

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я твой личный Telegram-бот 🚀")

@dp.message(Command("quote"))
async def quote_handler(message: Message):
    quote = get_random_quote()
    text = format_quote(quote)
    await message.answer(
        text,
        reply_markup = quote_keyboard
)

@dp.callback_query()
async def new_quote_handler(callback: CallbackQuery):
    quote = get_random_quote()
    text = format_quote(quote)
    await callback.answer()
    await callback.message.edit_text(
        text,
        reply_markup = quote_keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
