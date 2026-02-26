import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from database.connection import init_db
from bot.handlers import commands, entries
from bot.scheduler import setup_scheduler

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    token = os.environ["TG_TOKEN"]

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(entries.router)

    await init_db()
    logger.info("Database initialized")

    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("Scheduler started")

    logger.info("Starting bot polling")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
