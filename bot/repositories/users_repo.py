from bot.db.connection import get_connection

class UsersRepository:
    async def create_if_not_exists(self, user_id, username):
        async with get_connection() as db:
            await db.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
            await db.commit()

    async def get_by_id(self, user_id):
        async with get_connection() as db:
            async with db.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row

    async def update_basic_info(self, user_id, username):
        async with get_connection() as db:
            await db.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
            await db.commit()
