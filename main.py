import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
import misc
from handlers import main_router
from scheduler.scheduler import scheduler


async def start_bot():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    )
    dp = Dispatcher()

    dp.startup.register(misc.on_start)
    dp.shutdown.register(misc.on_shutdown)
    dp.include_router(main_router)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
