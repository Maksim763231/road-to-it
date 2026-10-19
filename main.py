import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database.db import create_tables

from handlers.motivation import router as motivation_router
from handlers.start import router as start_router
from services.scheduler import start_scheduler
from handlers.settings import router as settings_router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

dp = Dispatcher()
dp.include_router(motivation_router)
dp.include_router(start_router)
dp.include_router(settings_router)

async def main():
    create_tables()
    start_scheduler(bot)
    await dp.start_polling(bot)
    
async def main():
    start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
