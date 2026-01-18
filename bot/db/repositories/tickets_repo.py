from bot.db.connection import get_connection

class TicketsRepository:
    async def create_ticket(self, user_id, origin, destination, flight_date, price, currency):
        async with get_connection() as db:
            await db.execute("""
                INSERT INTO tickets (user_id, origin, destination, flight_date, price, currency)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, origin, destination, flight_date, price, currency))
            await db.commit()

    async def get_by_user(self, user_id):
        async with get_connection() as db:
            # Joining with users to get full name (though user_id is usually enough, user request specifically asked for name in history)
            query = """
                SELECT t.ticket_id, t.origin, t.destination, t.flight_date, t.price, t.currency, u.full_name 
                FROM tickets t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.user_id = ?
                ORDER BY t.created_at DESC
            """
            db.row_factory = lambda cursor, row: {
                "ticket_id": row[0], "origin": row[1], "destination": row[2], 
                "flight_date": row[3], "price": row[4], "currency": row[5], "full_name": row[6]
            }
            async with db.execute(query, (user_id,)) as cursor:
                return await cursor.fetchall()
