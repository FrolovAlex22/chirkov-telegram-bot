import logging.config

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import Config, load_config
from config.logging_settings import logging_config
from database.engine import create_db, drop_db
from handlers import (
    admin_handlers,
    other_handlers,
    user_handlers,
)


config: Config = load_config()

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def on_startup(bot):

    # run_param = True
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    logger.info("Бот лёг")


async def main():
    logger.info("Начало работы бота")
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(admin_handlers.admin_router)
    dp.include_router(user_handlers.user_router)
    dp.include_router(other_handlers.other_router)
    await dp.start_polling(bot)

asyncio.run(main())
