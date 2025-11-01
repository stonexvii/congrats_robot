from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ai_gpt import GPTMessage
from ai_gpt import ai_client
from ai_gpt.enums import GPTRole
from database import requests
from keyboards import ikb_remind_menu

storage = MemoryStorage()
scheduler = AsyncIOScheduler()


async def send_reminder(user_tg_id: int, data: dict, bot: Bot):
    task_id = data.pop('task_id')
    msg_list = GPTMessage('reminder_text')
    msg_list.update(GPTRole.USER, str(data))
    response = await ai_client.request(msg_list, bot)
    await bot.send_message(
        chat_id=user_tg_id,
        text=response,
        reply_markup=ikb_remind_menu(task_id),
    )

def schedule_event(user_tg_id: int, data: dict, bot: Bot):
    reminder = data.pop('reminder')
    scheduler.add_job(
        send_reminder,
        trigger="date",
        run_date=reminder,
        args=[user_tg_id, data, bot],
    )


async def start_all_tasks(bot: Bot):
    tasks = await requests.get_all_tasks()
    for task in tasks:
        schedule_event(task.user_id, task.as_kwargs(), bot)
