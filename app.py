import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from database.engine import create_db, drop_db
from handlers import (
    admin_handlers,
    other_handlers,
    ceramics_handlers,
    vr_handlers,
    art_gallery_handlers,
    event_handlers
)


config: Config = load_config()


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
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(admin_handlers.admin_router)
    dp.include_router(ceramics_handlers.ceramics_router)
    dp.include_router(vr_handlers.vr_router)
    dp.include_router(art_gallery_handlers.art_router)
    dp.include_router(event_handlers.event_router)
    dp.include_router(other_handlers.other_router)
    await dp.start_polling(bot)

asyncio.run(main())
