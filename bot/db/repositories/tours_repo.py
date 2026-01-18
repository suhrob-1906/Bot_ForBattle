from bot.db.connection import get_connection

class ToursRepository:
    async def get_all_active(self, offset=0, limit=5, hot_only=False):
        async with get_connection() as db:
            query = "SELECT * FROM tours WHERE active = 1"
            params = []
            if hot_only:
                query += " AND hot = 1"
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            db.row_factory = lambda cursor, row: {
                "tour_id": row[0], "title": row[1], "country": row[2], "city": row[3],
                "duration_days": row[4], "price_from": row[5], "currency": row[6],
                "description": row[7], "included": row[8], "hotel_stars": row[9],
                "hot": row[10], "active": row[11]
            }
            async with db.execute(query, params) as cursor:
                return await cursor.fetchall()

    async def get_by_id(self, tour_id):
        async with get_connection() as db:
            db.row_factory = lambda cursor, row: {
                "tour_id": row[0], "title": row[1], "country": row[2], "city": row[3],
                "duration_days": row[4], "price_from": row[5], "currency": row[6],
                "description": row[7], "included": row[8], "hotel_stars": row[9],
                "hot": row[10], "active": row[11]
            }
            async with db.execute("SELECT * FROM tours WHERE tour_id = ?", (tour_id,)) as cursor:
                return await cursor.fetchone()

    async def create_tour(self, data):
        async with get_connection() as db:
            await db.execute("""
                INSERT INTO tours (title, country, city, duration_days, price_from, currency, description, included, hotel_stars, hot, active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            await db.commit()

    async def delete_tour(self, tour_id):
        async with get_connection() as db:
            await db.execute("UPDATE tours SET active = 0 WHERE tour_id = ?", (tour_id,))
            await db.commit()
