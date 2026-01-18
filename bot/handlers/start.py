from aiogram import Router, types, F
from aiogram.filters import Command
from bot.db.repositories.users_repo import UsersRepository
from bot.keyboards.reply import lang_inline_kb, main_menu_kb
from bot.texts.localization import get_text

router = Router()
users_repo = UsersRepository()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user = await users_repo.get_user(user_id)
    if not user:
        await users_repo.upsert_user(user_id, message.from_user.username, message.from_user.full_name)
        await message.answer(get_text("ru", "start_new"), reply_markup=lang_inline_kb())
    else:
        lang = user[3]
        if not lang:
            await message.answer(get_text("ru", "start_new"), reply_markup=lang_inline_kb())
        else:
            await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))

@router.message(F.text.in_(["Языки", "Tillar"]))
async def cmd_languages(message: types.Message):
    await message.answer(get_text("ru", "lang_select"), reply_markup=lang_inline_kb())

@router.callback_query(F.data.startswith("setlang_"))
async def cb_setlang(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    await users_repo.set_language(call.from_user.id, lang)
    await call.message.delete()
    await call.message.answer(get_text(lang, "lang_saved"), reply_markup=main_menu_kb(lang))
    await call.answer()
