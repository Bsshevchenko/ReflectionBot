import aiosqlite
from datetime import datetime, timedelta
from database.connection import get_db_path


async def add_user(telegram_id: int, username: str | None) -> None:
    async with aiosqlite.connect(get_db_path()) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
            (telegram_id, username),
        )
        await db.commit()


async def get_user(telegram_id: int) -> dict | None:
    async with aiosqlite.connect(get_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def add_entry(telegram_id: int, content: str) -> None:
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute(
            "SELECT id FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return
            user_id = row[0]

        await db.execute(
            "INSERT INTO entries (user_id, content) VALUES (?, ?)",
            (user_id, content),
        )
        await db.commit()


async def get_weekly_entries(telegram_id: int) -> list[str]:
    week_ago = datetime.utcnow() - timedelta(days=7)
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute(
            """
            SELECT e.content
            FROM entries e
            JOIN users u ON e.user_id = u.id
            WHERE u.telegram_id = ? AND e.created_at >= ?
            ORDER BY e.created_at ASC
            """,
            (telegram_id, week_ago.isoformat()),
        ) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def get_all_users_with_weekly_entries() -> list[int]:
    week_ago = datetime.utcnow() - timedelta(days=7)
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute(
            """
            SELECT DISTINCT u.telegram_id
            FROM users u
            JOIN entries e ON e.user_id = u.id
            WHERE e.created_at >= ?
            """,
            (week_ago.isoformat(),),
        ) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
