from aiogram import Router, types, F
from aiogram.filters import Command
from bot.keyboards.reply import lang_kb, main_menu
from bot.db.repositories.users_repo import UsersRepository
from bot.texts.localization import get_text

router = Router()
user_repo = UsersRepository()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    if not user:
        await user_repo.upsert_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
        await message.answer("Выберите язык / Tilni tanlang:", reply_markup=lang_kb())
        return

    lang = user[3]
    if not lang or lang not in ["ru", "uz"]:
        await message.answer("Выберите язык / Tilni tanlang:", reply_markup=lang_kb())
    else:
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))

@router.message(Command("languages"))
async def lang_cmd(message: types.Message):
    await message.answer("Выберите язык / Tilni tanlang:", reply_markup=lang_kb())

@router.callback_query(F.data.startswith("lang_"))
async def lang_cb(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    await user_repo.set_language(call.from_user.id, lang)
    await call.message.delete()
    await call.message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
