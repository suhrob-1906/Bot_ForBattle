import asyncio
from aiogram import Bot, Dispatcher
from bot.config import settings
from bot.db.init_db import init_db
from bot.handlers import start, booking, hot_tours

async def main():
    await init_db()
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(booking.router)
    dp.include_router(hot_tours.router)
    
    await dp.start_polling(bot)
