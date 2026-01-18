from datetime import datetime
from bot.db.connection import get_connection

class PaymentsRepository:
    async def create_payment(self, request_id, user_id, amount, currency):
        async with get_connection() as db:
            cursor = await db.execute("""
                INSERT INTO payments (request_id, user_id, amount, currency, status)
                VALUES (?, ?, ?, ?, ?)
            """, (request_id, user_id, amount, currency, "pending"))
            await db.commit()
            return cursor.lastrowid

    async def mark_paid(self, payment_id):
        async with get_connection() as db:
            await db.execute("""
                UPDATE payments SET status = 'paid', paid_at = ?
                WHERE payment_id = ?
            """, (datetime.now(), payment_id))
            await db.commit()

    async def get_by_id(self, payment_id):
        async with get_connection() as db:
            db.row_factory = lambda cursor, row: {"payment_id": row[0], "request_id": row[1], "amount": row[3], "currency": row[4], "status": row[5]}
            async with db.execute("SELECT * FROM payments WHERE payment_id = ?", (payment_id,)) as cursor:
                return await cursor.fetchone()
