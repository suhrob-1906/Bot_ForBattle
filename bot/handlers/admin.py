from aiogram import Router, types, F
from aiogram.filters import Command
from bot.config import settings
from bot.db.connection import get_connection

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        await message.answer("Access denied")
        return

    stats = await get_stats()
    text = (
        f"ADMIN PANEL\n\n"
        f"Users: {stats['users']}\n"
        f"Tours: {stats['tours']}\n"
        f"Requests: {stats['requests']}\n"
        f"Payments: {stats['payments']}\n\n"
        f"Use /broadcast <text> to send message to all users"
    )
    await message.answer(text)

@router.message(Command("broadcast"))
async def admin_broadcast(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return
    
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("Usage: /broadcast <message>")
        return

    count = await broadcast_message(message.bot, text)
    await message.answer(f"Broadcast sent to {count} users")

async def get_stats():
    async with get_connection() as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c:
            users = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM tours") as c:
            tours = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM requests") as c:
            reqs = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM payments") as c:
            pays = (await c.fetchone())[0]
    return {"users": users, "tours": tours, "requests": reqs, "payments": pays}

async def broadcast_message(bot, text):
    count = 0
    async with get_connection() as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            async for row in cursor:
                try:
                    await bot.send_message(row[0], text)
                    count += 1
                except:
                    pass
    return count
