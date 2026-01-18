from bot.db.connection import get_connection

class UsersRepository:
    async def upsert_user(self, user_id, username, full_name):
        async with get_connection() as db:
            await db.execute("""
                INSERT INTO users (user_id, username, full_name)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                full_name=excluded.full_name
            """, (user_id, username, full_name))
            await db.commit()

    async def get_user(self, user_id):
        async with get_connection() as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def set_language(self, user_id, language):
        async with get_connection() as db:
            await db.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
            await db.commit()

    async def get_all_users(self):
        async with get_connection() as db:
            async with db.execute("SELECT user_id FROM users") as cursor:
                return await cursor.fetchall()
