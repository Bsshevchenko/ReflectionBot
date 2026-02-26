import os
import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

logger = logging.getLogger(__name__)


class AllowedUsersMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        raw = os.environ.get("ALLOWED_USER_IDS", "")
        self.allowed = {int(uid.strip()) for uid in raw.split(",") if uid.strip()}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        update: Update = data.get("event_update")
        user = data.get("event_from_user")

        if user is None or user.id not in self.allowed:
            uid = user.id if user else "unknown"
            logger.warning(f"Blocked unauthorized user: {uid}")
            return

        return await handler(event, data)
