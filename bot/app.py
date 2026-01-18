import asyncio
from aiogram import Bot, Dispatcher
from bot.config import settings
from bot.db.init_db import init_db
from bot.handlers import start, tours_catalog, selection_fsm, my_requests, payments, contacts, admin

async def main():
    await init_db()
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(contacts.router)
    dp.include_router(tours_catalog.router)
    dp.include_router(selection_fsm.router)
    dp.include_router(my_requests.router)
    dp.include_router(payments.router)
    
    await dp.start_polling(bot)
