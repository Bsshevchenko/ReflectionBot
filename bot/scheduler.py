import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from database.queries import get_all_users_with_weekly_entries, get_weekly_entries
from ai.analyzer import generate_weekly_report

logger = logging.getLogger(__name__)

MOSCOW_TZ = pytz.timezone("Europe/Moscow")


async def send_weekly_reports(bot) -> None:
    logger.info("Running weekly report job")
    user_ids = await get_all_users_with_weekly_entries()

    for telegram_id in user_ids:
        try:
            entries = await get_weekly_entries(telegram_id)
            if not entries:
                continue
            report = await generate_weekly_report(entries)
            await bot.send_message(
                telegram_id,
                f"📊 <b>Твой недельный отчёт:</b>\n\n{report}",
                parse_mode="HTML",
            )
            logger.info(f"Sent weekly report to user {telegram_id}")
        except Exception:
            logger.exception(f"Failed to send report to user {telegram_id}")


def setup_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=MOSCOW_TZ)
    scheduler.add_job(
        send_weekly_reports,
        trigger=CronTrigger(day_of_week="sun", hour=12, minute=0, timezone=MOSCOW_TZ),
        args=[bot],
        id="weekly_report",
        replace_existing=True,
    )
    return scheduler
