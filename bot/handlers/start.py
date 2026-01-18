from aiogram import Router, types, F
from aiogram.filters import Command
from bot.keyboards.reply import language_keyboard, main_menu
from bot.db.repositories.users_repo import UsersRepository
from bot.texts.localization import get_text

router = Router()
user_repo = UsersRepository()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await user_repo.upsert_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer("Выберите язык / Tilni tanlang:", reply_markup=language_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def language_selected(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    await user_repo.set_language(call.from_user.id, lang)
    await call.message.delete()
    await call.message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
    await call.answer()
