from aiogram import Router, F
from aiogram.types import Message

from database.queries import add_user, add_entry

router = Router()


@router.message(F.text)
async def handle_entry(message: Message) -> None:
    await add_user(message.from_user.id, message.from_user.username)
    await add_entry(message.from_user.id, message.text)
    await message.answer("✅ Мысль записана")
