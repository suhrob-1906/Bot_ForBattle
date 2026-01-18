from bot.db.connection import get_connection

class RequestsRepository:
    async def create_request(self, data):
        async with get_connection() as db:
            cursor = await db.execute("""
                INSERT INTO requests (user_id, request_type, tour_id, status, travel_month, budget_value, budget_currency, people_count, preferences, phone, contact_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("user_id"), data.get("request_type"), data.get("tour_id"), "new",
                data.get("travel_month"), data.get("budget_value"), data.get("budget_currency"),
                data.get("people_count"), data.get("preferences"), data.get("phone"), data.get("contact_method")
            ))
            await db.commit()
            return cursor.lastrowid

    async def get_by_user(self, user_id):
        async with get_connection() as db:
            db.row_factory = lambda cursor, row: {
                "request_id": row[0], "request_type": row[2], "tour_id": row[3], "status": row[4], "created_at": row[12]
            }
            async with db.execute("SELECT * FROM requests WHERE user_id = ? ORDER BY created_at DESC", (user_id,)) as cursor:
                return await cursor.fetchall()
    
    async def get_by_id(self, request_id):
        async with get_connection() as db:
            db.row_factory = lambda cursor, row: {
                "request_id": row[0], "user_id": row[1], "request_type": row[2], "tour_id": row[3], "status": row[4], "created_at": row[12]
            }
            async with db.execute("SELECT * FROM requests WHERE request_id = ?", (request_id,)) as cursor:
                return await cursor.fetchone()

    async def update_status(self, request_id, status):
        async with get_connection() as db:
            await db.execute("UPDATE requests SET status = ? WHERE request_id = ?", (status, request_id))
            await db.commit()

    async def get_all_active(self):
        async with get_connection() as db:
            db.row_factory = lambda cursor, row: {
                "request_id": row[0], "user_id": row[1], "request_type": row[2], "status": row[4], "created_at": row[12]
            }
            async with db.execute("SELECT * FROM requests WHERE status != 'canceled' ORDER BY created_at DESC") as cursor:
                return await cursor.fetchall()

    async def cancel_request(self, request_id):
        return await self.update_status(request_id, "canceled")
