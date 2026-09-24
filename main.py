import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.motivation import router as motivation_router
from handlers.start import router as start_router
from services.scheduler import start_scheduler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

dp = Dispatcher()
dp.include_router(motivation_router)
dp.include_router(start_router)

async def main():
    start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
