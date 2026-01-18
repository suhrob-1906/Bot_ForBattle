from aiogram import Router, types

router = Router()

@router.message()
async def handle_unknown(message: types.Message):
    await message.answer("Не понял, открой меню")
