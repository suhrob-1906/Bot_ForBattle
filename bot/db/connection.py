import aiosqlite
from bot.config import settings

def get_connection():
    return aiosqlite.connect(settings.DB_PATH)
