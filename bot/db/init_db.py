from bot.db.connection import get_connection

async def init_db():
    async with get_connection() as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                language TEXT DEFAULT 'ru',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                from_city TEXT,
                to_city TEXT,
                depart_date TEXT,
                return_date TEXT,
                budget_value REAL,
                budget_currency TEXT,
                passengers INTEGER,
                hotel TEXT,
                meals TEXT,
                fare_name TEXT,
                price_value REAL,
                price_currency TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
