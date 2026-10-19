from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from quotes import get_random_quote
from handlers.motivation import format_quote
from repositories.user_repository import get_all_users, get_user

scheduler = AsyncIOScheduler()


async def send_daily_quote(bot, chat_id: int):
    user = get_user(chat_id)

    if user is None or not user.enabled:
        return

    quote = get_random_quote()
    text = format_quote(quote)

    await bot.send_message(
        chat_id=user.chat_id,
        text=text,
    )


def schedule_user(bot, user):
    job_id = f"daily_quote_{user.chat_id}"

    existing_job = scheduler.get_job(job_id)

    if existing_job:
        scheduler.remove_job(job_id)

    if not user.enabled:
        return

    hour, minute = map(int, user.time.split(":"))

    scheduler.add_job(
        send_daily_quote,
        trigger=CronTrigger(
            hour=hour,
            minute=minute,
            timezone=ZoneInfo(user.timezone),
        ),
        args=[bot, user.chat_id],
        id=job_id,
        replace_existing=True,
    )


def start_scheduler(bot):
    scheduler.start()

    for user in get_all_users():
        schedule_user(bot, user)