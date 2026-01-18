from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    text = (
        "/start - Start bot\n"
        "/help - Show help"
    )
    await message.answer(text)
