from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.queries import add_user, get_weekly_entries
from ai.analyzer import generate_weekly_report

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "👋 Привет! Я бот для личной рефлексии.\n\n"
        "Просто пиши мне свои мысли, переживания и наблюдения в любой момент — "
        "я буду сохранять их, а каждое воскресенье в 12:00 МСК пришлю тебе "
        "подробный анализ твоей недели.\n\n"
        "Используй /help, чтобы узнать больше."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "📖 <b>Как пользоваться ботом:</b>\n\n"
        "• Просто отправь любое текстовое сообщение — я его сохраню\n"
        "• Каждое воскресенье в 12:00 МСК получишь анализ недели\n\n"
        "<b>Команды:</b>\n"
        "/start — регистрация\n"
        "/report — получить отчёт прямо сейчас\n"
        "/help — эта справка",
        parse_mode="HTML",
    )


@router.message(Command("report"))
async def cmd_report(message: Message) -> None:
    await add_user(message.from_user.id, message.from_user.username)

    entries = await get_weekly_entries(message.from_user.id)
    if not entries:
        await message.answer(
            "📭 За последние 7 дней нет ни одной записи.\n"
            "Просто напиши мне что-нибудь — и я сохраню твои мысли!"
        )
        return

    await message.answer("⏳ Анализирую твои записи, подожди немного...")

    try:
        report = await generate_weekly_report(entries)
        await message.answer(f"📊 <b>Твой недельный отчёт:</b>\n\n{report}", parse_mode="HTML")
    except Exception as e:
        await message.answer(
            "❌ Не удалось сгенерировать отчёт. Попробуй позже."
        )
        raise
