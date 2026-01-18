from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.db.repositories.users_repo import UsersRepository
from bot.db.repositories.tours_repo import BookingsRepository
from bot.texts.localization import get_text
from bot.keyboards.reply import main_menu_kb, cancel_reply_kb, history_paging_kb

router = Router()
users_repo = UsersRepository()
bookings_repo = BookingsRepository()

class StepStates(StatesGroup):
    dest = State()
    date = State()
    budget = State()
    pax = State()
    wishes = State()

@router.message(F.text.in_(["Контакты", "Aloqa"]))
async def show_contacts(message: types.Message):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3] if user else 'ru'
    await message.answer(get_text(lang, "contacts_text"))

@router.message(F.text.in_(["Помощь", "Yordam"]))
async def show_help(message: types.Message):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3] if user else 'ru'
    await message.answer(get_text(lang, "help_text"))

@router.message(F.text.in_(["Подобрать тур", "Tur tanlash"]))
@router.message(F.command == "tour")
async def start_tour(message: types.Message, state: FSMContext):
    user = await users_repo.get_user(message.from_user.id)
    if not user:
        user = await users_repo.upsert_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
        lang = 'ru'
    else:
        lang = user[3]
    
    await state.clear()
    await state.update_data(lang=lang)
    await state.set_state(StepStates.dest)
    await message.answer(get_text(lang, "q_dest"), reply_markup=cancel_reply_kb(lang))

@router.message(StepStates.dest)
async def state_dest(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return

    await state.update_data(to_city=message.text)
    await state.set_state(StepStates.date)
    await message.answer(get_text(lang, "q_date"), reply_markup=cancel_reply_kb(lang))

@router.message(StepStates.date)
async def state_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return

    await state.update_data(depart_date=message.text)
    await state.set_state(StepStates.budget)
    await message.answer(get_text(lang, "q_budget"), reply_markup=cancel_reply_kb(lang))

@router.message(StepStates.budget)
async def state_budget(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
    
    # Allow loose input, but try to find a digit if possible, otherwise just save text
    # The prompt says "(in USD)", so we assume USD
    
    await state.update_data(budget_value=message.text) # Save as text to handle "600" or "approx 600" if we want loose
    # But DB expects REAL for budget_value. Let's try to extract int, or default to 0
    try:
        val = float(''.join(filter(str.isdigit, message.text)))
    except:
        val = 0.0
    
    await state.update_data(budget_val_real=val)
    
    await state.set_state(StepStates.pax)
    await message.answer(get_text(lang, "q_pax"), reply_markup=cancel_reply_kb(lang))

@router.message(StepStates.pax)
async def state_pax(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
        
    # Like budget, save loosely or strict? User log showed "3"
    try:
        val = int(message.text)
    except:
        val = 1
        
    await state.update_data(pax=val)
    await state.set_state(StepStates.wishes)
    await message.answer(get_text(lang, "q_wishes"), reply_markup=cancel_reply_kb(lang))

@router.message(StepStates.wishes)
async def state_wishes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return

    wishes = message.text
    
    # Save to DB
    # Mapping loose fields to our schema:
    # from_city -> "Tashkent" (default)
    # to_city -> dest
    # depart_date -> date
    # return_date -> "" (none)
    # budget_value -> budget line
    # budget_currency -> "USD"
    # passengers -> pax
    # hotel -> wishes (storage hack)
    # meals -> "Any" (or part of wishes)
    
    save_data = {
        "user_id": message.from_user.id,
        "from_city": "Tashkent", # Default
        "to_city": data['to_city'],
        "depart_date": data['depart_date'],
        "return_date": "", 
        "budget_value": data['budget_val_real'],
        "budget_currency": "USD",
        "passengers": data['pax'],
        "hotel": wishes, 
        "meals": "Any",
        "fare_name": "Custom",
        "price_value": 0,
        "price_currency": "USD",
        "status": "pending"
    }
    
    booking_id = await bookings_repo.create_booking(save_data)
    
    await state.clear()
    await message.answer(get_text(lang, "booking_created").format(booking_id), reply_markup=main_menu_kb(lang))

@router.message(F.text.in_(["Мои заявки", "Mening buyurtmalarim"]))
async def cmd_history(message: types.Message):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3] if user else 'ru'
    await show_history_page(message.from_user.id, lang, message, 0)

@router.callback_query(F.data.startswith("hist_"))
async def cb_history(call: types.CallbackQuery):
    user = await users_repo.get_user(call.from_user.id)
    lang = user[3] if user else 'ru'
    offset = int(call.data.split("_")[1])
    await call.message.delete()
    await show_history_page(call.from_user.id, lang, call.message, offset)

async def show_history_page(user_id, lang, message, offset):
    limit = 5
    items = await bookings_repo.get_by_user(user_id, limit, offset)
    if not items and offset == 0:
        await message.answer(get_text(lang, "history_empty"))
        return
    
    text = f"{get_text(lang, 'history_title')}\n\n"
    for item in items:
        # Format for history
        text += (
            f"#{item['id']} | {item['to_city']}\n"
            f"Date: {item['depart_date']}\n"
            f"Budget: {item['budget_value']}$\n"
            f"Wishes: {item['hotel']}\n"
            f"--------------\n"
        )
        
    total = offset + limit + 1 if len(items) == limit else offset + len(items)
    await message.answer(text, reply_markup=history_paging_kb(lang, offset, limit, total))
