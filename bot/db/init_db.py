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
            CREATE TABLE IF NOT EXISTS tours (
                tour_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                country TEXT,
                city TEXT,
                duration_days INTEGER,
                price_from REAL,
                currency TEXT,
                description TEXT,
                included TEXT,
                hotel_stars INTEGER,
                image_url TEXT,
                hot INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                request_type TEXT,
                tour_id INTEGER NULL,
                status TEXT DEFAULT 'new',
                travel_month TEXT NULL,
                budget_value REAL NULL,
                budget_currency TEXT NULL,
                people_count INTEGER NULL,
                preferences TEXT NULL,
                phone TEXT NULL,
                contact_method TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                user_id INTEGER,
                amount REAL,
                currency TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_at TIMESTAMP NULL
            )
        """)
        
        async with db.execute("SELECT COUNT(*) FROM tours") as cursor:
            count = await cursor.fetchone()
            if count[0] == 0:
                await seed_tours(db)
        
        await db.commit()

async def seed_tours(db):
    tours = [
        ("Maldive Paradise", "Maldives", "Male", 7, 1500, "USD", "Luxury stay", "All inclusive", 5, "https://images.unsplash.com/photo-1514282401047-d79a71a590e8", 1, 1),
        ("Turkish Delight", "Turkey", "Antalya", 7, 800, "USD", "Family resort", "All inclusive", 5, "https://images.unsplash.com/photo-1527668752968-14dc70a27c95", 1, 1),
        ("Dubai Future", "UAE", "Dubai", 5, 1200, "USD", "Modern city tour", "Breakfast", 4, "https://images.unsplash.com/photo-1512453979798-5ea904ac848e", 0, 1),
        ("European Dream", "France", "Paris", 5, 2000, "EUR", "Romantic getaway", "Breakfast", 4, "https://images.unsplash.com/photo-1502602898657-3e91760cbb34", 0, 1),
        ("Samarkand Ancient", "Uzbekistan", "Samarkand", 3, 200, "USD", "History tour", "Guide + Transport", 3, "https://images.unsplash.com/photo-1628189873406-880c541797e8", 0, 1),
    ]
    await db.executemany("""
        INSERT INTO tours (title, country, city, duration_days, price_from, currency, description, included, hotel_stars, image_url, hot, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tours)
