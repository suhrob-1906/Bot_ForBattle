from aiogram import Router, types, F
from bot.db.repositories.users_repo import UsersRepository
from bot.texts.localization import get_text

router = Router()
user_repo = UsersRepository()

@router.message(F.text.in_({"📞 Контакты", "❓ FAQ", "📞 Kontaktlar"}))
async def show_info(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user else "ru"
    
    if "FAQ" in message.text:
         await message.answer(get_text(lang, "faq_text"))
    else:
         await message.answer(get_text(lang, "contacts_text"))
