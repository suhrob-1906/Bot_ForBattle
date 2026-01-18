from aiogram import Router, types, F
from bot.db.repositories.requests_repo import RequestsRepository
from bot.db.repositories.tickets_repo import TicketsRepository
from bot.db.repositories.users_repo import UsersRepository
from bot.texts.localization import get_all_variants, get_text

router = Router()
requests_repo = RequestsRepository()
tickets_repo = TicketsRepository()
user_repo = UsersRepository()

@router.message(F.text.in_(get_all_variants("btn_my_requests")))
async def my_requests_and_history(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user else "ru"
    
    # Show Requests
    reqs = await requests_repo.get_by_user(message.from_user.id)
    if reqs:
        await message.answer(get_text(lang, "btn_my_requests"))
        for req in reqs:
            # Shortened check for demo
            await message.answer(f"Application #{req['request_id']} ({req['status']})")
    
    # Show Tickets History
    tickets = await tickets_repo.get_by_user(message.from_user.id)
    if tickets:
        header = get_text(lang, "Msg_History_Header")
        for t in tickets:
            header += f"\n👤 {t['full_name']}\n✈️ {t['origin']} -> {t['destination']}\n📅 {t['flight_date']}\n💰 {t['price']} {t['currency']}\n-----------------"
        await message.answer(header)
    else:
        await message.answer(get_text(lang, "Msg_History_Empty"))
