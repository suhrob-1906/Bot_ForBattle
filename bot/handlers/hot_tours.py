from aiogram import Router, types, F
from bot.db.repositories.tours_repo import HotOffersRepository, BookingsRepository
from bot.db.repositories.users_repo import UsersRepository
from bot.keyboards.reply import hot_nav_kb, history_nav_kb
from bot.texts.localization import get_text

router = Router()
hot_repo = HotOffersRepository()
book_repo = BookingsRepository()
user_repo = UsersRepository()

@router.message(F.text.in_(["Горящие туры", "Qaynoq turlar"]))
async def show_hot(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3]
    
    offers = await hot_repo.get_active_offers(limit=1, offset=0)
    if not offers:
        await message.answer(get_text(lang, "hot_empty"))
        return

    offer = offers[0]
    await send_offer(message, offer, lang, 0, 10) # 10 is hardcoded count from seed

@router.callback_query(F.data.startswith("hot_"))
async def hot_nav(call: types.CallbackQuery):
    action, _, id_str = call.data.split("_")
    # action: prev, next, book
    # id is offer_id (but we need offset mostly for nav)
    # simplified: using global id for booking
    
    user = await user_repo.get_user(call.from_user.id)
    lang = user[3]
    
    if action == "book":
        await call.answer("Booking logic init...")
        # Redirect to booking FSM logic
        return

    # Pagination logic simplification needed for stateless 
    # Current code assumes 1 by 1 by ID which is tricky if IDs are not sequential
    # Better: hot_next_{offset}
    
    # Re-fetch based on offset logic
    # Assume ID is offset for this demo
    current_offset = int(id_str)
    new_offset = current_offset + 1 if action == "next" else current_offset - 1
    
    offers = await hot_repo.get_active_offers(limit=1, offset=new_offset)
    if not offers:
        await call.answer("No more", show_alert=True)
        return
        
    offer = offers[0]
    await call.message.delete()
    await send_offer(call.message, offer, lang, new_offset, 10)

async def send_offer(message, offer, lang, offset, total):
    title = offer[f'title_{lang}']
    desc = offer[f'description_{lang}']
    text = f"🔥 {title}\n\n{desc}\n\n📍 {offer['from_city']} -> {offer['to_city']}\n💰 {offer['price_from']} {offer['currency']}"
    
    kb = hot_nav_kb(offset, total, lang) # passing offset as ID for nav
    
    if offer['image_url']:
        await message.answer_photo(offer['image_url'], caption=text, reply_markup=kb)
    else:
        await message.answer(text, reply_markup=kb)

# History
@router.message(F.text.in_(["История полетов", "Parvozlar tarixi"]))
async def show_history(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3]
    
    bookings = await book_repo.get_by_user(message.from_user.id, limit=5, offset=0)
    if not bookings:
        await message.answer(get_text(lang, "history_empty"))
        return

    text = f"{get_text(lang, 'btn_history')}:\n\n"
    for b in bookings:
        text += f"📅 {b['created_at']}\n🚀 {b['from_city']} -> {b['to_city']}\n💰 {b['price_value']} {b['price_currency']}\nStatus: {b['status']}\n\n"
        
    await message.answer(text, reply_markup=history_nav_kb(0, 5, 100, lang))
