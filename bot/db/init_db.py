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
                price_value REAL,
                price_currency TEXT,
                fare_name TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS hot_offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_ru TEXT,
                title_uz TEXT,
                description_ru TEXT,
                description_uz TEXT,
                from_city TEXT,
                to_city TEXT,
                price_from REAL,
                currency TEXT,
                image_url TEXT,
                active INTEGER DEFAULT 1
            )
        """)
        
        async with db.execute("SELECT COUNT(*) FROM hot_offers") as cursor:
            count = (await cursor.fetchone())[0]
            
        if count == 0:
            offers = [
                ("Отдых в Анталии", "Antaliyada dam olish", "Все включено, 7 ночей", "Hammasi ichida, 7 tun", "Ташкент", "Анталья", 800, "USD", "https://example.com/antalya.jpg", 1),
                ("Дубайский Шоппинг", "Dubay Shopping", "Отель 4*, завтраки", "Mehmonxona 4*, nonushta", "Ташкент", "Дубай", 600, "USD", "https://example.com/dubai.jpg", 1),
                ("Мальдивы", "Maldiv orollari", "Бунгало на воде", "Suv ustidagi bungalow", "Ташкент", "Мале", 2500, "USD", "https://example.com/maldives.jpg", 1),
                ("Стамбул Классик", "Istanbul Klassik", "Экскурсии включены", "Ekskursiyalar kiritilgan", "Ташкент", "Стамбул", 550, "USD", "https://example.com/istanbul.jpg", 1),
                ("Шарм-Эль-Шейх", "Sharm-El-Sheyx", "Красное море, дайвинг", "Qizil dengiz, dayving", "Ташкент", "Шарм", 700, "USD", "https://example.com/sharm.jpg", 1),
                ("Пхукет Экзотика", "Pxuket Ekzotika", "Тропический рай", "Tropik jannat", "Ташкент", "Пхукет", 1200, "USD", "https://example.com/phuket.jpg", 1),
                ("Самарканд Тур", "Samarqand Tur", "Исторический тур", "Tarixiy sayohat", "Ташкент", "Самарканд", 50, "USD", "", 1),
                ("Хива Сказка", "Xiva Ertagi", "Поездка в прошлое", "O'tmishga sayohat", "Ташкент", "Хива", 100, "USD", "", 1),
                ("Бали Релакс", "Bali Relaks", "Йога и серфинг", "Yoga va serfing", "Ташкент", "Денпасар", 1500, "USD", "https://example.com/bali.jpg", 1),
                ("Евротур", "Yevrotur", "Прага, Вена, Будапешт", "Praga, Vena, Budapesht", "Ташкент", "Европа", 1800, "USD", "https://example.com/euro.jpg", 1)
            ]
            await db.executemany("""
                INSERT INTO hot_offers (title_ru, title_uz, description_ru, description_uz, from_city, to_city, price_from, currency, image_url, active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, offers)
            await db.commit()
