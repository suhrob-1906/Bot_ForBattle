from aiogram import Router, types, F
from bot.db.repositories.users_repo import UsersRepository
from bot.texts.localization import get_text, get_all_variants

router = Router()
user_repo = UsersRepository()

@router.message(F.text.in_(get_all_variants("btn_contacts").union(get_all_variants("btn_faq"))))
async def show_info(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user else "ru"
    
    if message.text in get_all_variants("btn_faq"):
         await message.answer(get_text(lang, "faq_text"))
    else:
         await message.answer(get_text(lang, "contacts_text"))
