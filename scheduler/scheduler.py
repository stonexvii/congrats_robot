from aiogram import Bot, Dispatcher
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import asyncio

scheduler = AsyncIOScheduler()


async def send_birthday_reminder(user_tg_id: int, name: str, bot: Bot):
    await bot.send_message(
        chat_id=user_tg_id,
        text=f"🎉 Сегодня день рождения у {name}!",
    )


def schedule_event(user_id: int, name: str, event: str, date: datetime, bot):
    # remind_time = date - timedelta(days=1)
    scheduler.add_job(
        send_birthday_reminder,
        trigger="date",
        run_date=date,
        args=[user_id, name, bot],
        id=f'user_{user_id}',
        replace_existing=True,
    )
