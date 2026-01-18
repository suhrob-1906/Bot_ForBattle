from bot.db.connection import get_connection

class BookingsRepository:
    async def create_booking(self, data):
        async with get_connection() as db:
            cursor = await db.execute("""
                INSERT INTO bookings (
                    user_id, from_city, to_city, depart_date, return_date, 
                    budget_value, budget_currency, passengers, hotel, meals, 
                    fare_name, price_value, price_currency, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['user_id'], data['from_city'], data['to_city'], data['depart_date'], data['return_date'],
                data['budget_value'], data['budget_currency'], data['passengers'], data['hotel'], data['meals'],
                data['fare_name'], data['price_value'], data['price_currency'], data['status']
            ))
            await db.commit()
            return cursor.lastrowid

    async def get_by_user(self, user_id, limit=5, offset=0):
        async with get_connection() as db:
            query = """
                SELECT * FROM bookings 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """
            db.row_factory = lambda c, r: {
                "id": r[0], "user_id": r[1], "from_city": r[2], "to_city": r[3],
                "depart_date": r[4], "return_date": r[5], "budget_value": r[6],
                "budget_currency": r[7], "passengers": r[8], "hotel": r[9],
                "meals": r[10], "fare_name": r[11], "price_value": r[12], 
                "price_currency": r[13], "status": r[14], "created_at": r[15]
            }
            async with db.execute(query, (user_id, limit, offset)) as cursor:
                return await cursor.fetchall()

    async def get_by_id(self, booking_id):
        async with get_connection() as db:
            query = "SELECT * FROM bookings WHERE id = ?"
            db.row_factory = lambda c, r: {
                "id": r[0], "user_id": r[1], "from_city": r[2], "to_city": r[3],
                "depart_date": r[4], "return_date": r[5], "budget_value": r[6],
                "budget_currency": r[7], "passengers": r[8], "hotel": r[9],
                "meals": r[10], "fare_name": r[11], "price_value": r[12], 
                "price_currency": r[13], "status": r[14], "created_at": r[15]
            }
            async with db.execute(query, (booking_id,)) as cursor:
                return await cursor.fetchone()
            
    async def update_status(self, booking_id, status):
         async with get_connection() as db:
            await db.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
            await db.commit()
