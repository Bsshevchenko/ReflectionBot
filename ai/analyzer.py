import anthropic
import os

MODEL = "claude-sonnet-4-6"


def _build_prompt(entries: list[str]) -> str:
    numbered = "\n".join(f"{i + 1}. {entry}" for i, entry in enumerate(entries))
    return f"""Ты — внимательный психолог и коуч. Пользователь вёл дневник мыслей в течение недели.
Вот его записи:

{numbered}

Составь структурированный еженедельный отчёт на русском языке.
Используй HTML-теги для форматирования (отчёт будет отправлен в Telegram):
- <b>текст</b> — жирный
- <i>текст</i> — курсив
- <blockquote>текст</blockquote> — цитата/выделение

Структура отчёта — строго четыре раздела с эмодзи-заголовками:

🗂 <b>Основные темы недели</b>
Кратко перечисли главные темы и события через дефис (-).

💬 <b>Анализ эмоций</b>
Какие эмоции прослеживаются в записях, насколько они интенсивны.

🔍 <b>Причины и триггеры</b>
Что вызывало эти переживания, какие паттерны заметны.

✅ <b>Практические советы</b>
Конкретные рекомендации на следующую неделю через дефис (-).

Будь тёплым, поддерживающим и конкретным. Избегай общих фраз. Опирайся на детали из записей.
Не используй символы <, > нигде кроме HTML-тегов."""


async def generate_weekly_report(entries: list[str]) -> str:
    client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = await client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": _build_prompt(entries),
            }
        ],
    )

    return message.content[0].text
