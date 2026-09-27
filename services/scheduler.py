from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quotes import get_random_quote
from handlers.motivation import format_quote
from repositories.user_repository import get_all_users

async def test_job(bot):
    quote = get_random_quote()
    formatted_quote = format_quote(quote)
    users = get_all_users()
    for user in users:
        await bot.send_message(chat_id=user.chat_id, text=formatted_quote)


scheduler = AsyncIOScheduler()

def start_scheduler(bot):
    scheduler.add_job(
        test_job,
        'cron',
        hour = 8,
        minute=0,
        args=[bot]
    )

    scheduler.start()