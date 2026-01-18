import re
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.db.repositories.users_repo import UsersRepository
from bot.db.repositories.tours_repo import BookingsRepository
from bot.texts.localization import get_text
from bot.keyboards.reply import (
    main_menu_kb, cities_kb, cancel_reply_kb, currency_kb, pax_kb, 
    hotel_stars_kb, meals_kb, tariffs_inline_kb, payment_inline_kb, history_paging_kb
)

router = Router()
users_repo = UsersRepository()
bookings_repo = BookingsRepository()

class BookingStates(StatesGroup):
    origin = State()
    destination = State()
    date_out = State()
    date_ret = State()
    budget = State()
    pax = State()
    hotel = State()
    meals = State()
    tariff = State()

@router.message(F.text.in_(["Контакты", "Aloqa"]))
async def show_contacts(message: types.Message):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3]
    await message.answer(get_text(lang, "contacts_text"))

@router.message(F.text.in_(["Помощь", "Yordam"]))
async def show_help(message: types.Message):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3]
    await message.answer(get_text(lang, "help_text"))

@router.message(F.text.in_(["Оформить билет", "Chipta rasmiylashtirish"]))
@router.message(F.command == "ticket")
async def start_booking(message: types.Message, state: FSMContext):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3]
    await state.update_data(lang=lang)
    await state.set_state(BookingStates.origin)
    await message.answer(get_text(lang, "action_origin"), reply_markup=cities_kb(lang))

@router.message(BookingStates.origin)
async def state_origin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if message.text in ["Отмена", "Bekor qilish", "Cancel"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
        
    if message.text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "btn_other"), reply_markup=cancel_reply_kb(lang))
        return
        
    await state.update_data(origin=message.text)
    await state.set_state(BookingStates.destination)
    await message.answer(get_text(lang, "action_dest"), reply_markup=cities_kb(lang, exclude=message.text))

@router.message(BookingStates.destination)
async def state_dest(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish", "Cancel"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return

    if message.text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "btn_other"), reply_markup=cancel_reply_kb(lang))
        return
        
    if message.text == data.get('origin'):
        await message.answer(get_text(lang, "err_same_city"))
        return

    await state.update_data(dest=message.text)
    await state.set_state(BookingStates.date_out)
    await message.answer(get_text(lang, "action_date_out"), reply_markup=cancel_reply_kb(lang))

@router.message(BookingStates.date_out)
async def state_date_out(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return

    if not re.match(r"\d{2}\.\d{2}\.\d{4}", message.text):
        await message.answer(get_text(lang, "err_format"))
        return

    await state.update_data(date_out=message.text)
    await state.set_state(BookingStates.date_ret)
    await message.answer(get_text(lang, "action_date_ret"), reply_markup=cancel_reply_kb(lang))

@router.message(BookingStates.date_ret)
async def state_date_ret(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return

    if not re.match(r"\d{2}\.\d{2}\.\d{4}", message.text):
        await message.answer(get_text(lang, "err_format"))
        return

    await state.update_data(date_ret=message.text)
    await state.set_state(BookingStates.budget)
    await message.answer(get_text(lang, "action_budget"), reply_markup=cancel_reply_kb(lang))

@router.message(BookingStates.budget)
async def state_budget(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
    
    if not message.text.isdigit():
        await message.answer(get_text(lang, "err_number"))
        return

    await state.update_data(budget_val=int(message.text))
    
    # Implicitly move to currency
    await message.answer(get_text(lang, "action_currency"), reply_markup=currency_kb(lang))

@router.message(F.text.in_(["USD", "UZS"]))
async def state_currency(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if await state.get_state() != BookingStates.budget:
        return 

    await state.update_data(budget_curr=message.text)
    await state.set_state(BookingStates.pax)
    await message.answer(get_text(lang, "action_pax"), reply_markup=pax_kb(lang))

@router.message(BookingStates.pax)
async def state_pax(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
        
    if message.text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "btn_other"), reply_markup=cancel_reply_kb(lang))
        return

    if not message.text.isdigit():
        await message.answer(get_text(lang, "err_number"))
        return
    
    val = int(message.text)
    if val < 1 or val > 20:
        await message.answer(get_text(lang, "err_pax_range"))
        return

    await state.update_data(pax=val)
    await state.set_state(BookingStates.hotel)
    await message.answer(get_text(lang, "action_hotel"), reply_markup=hotel_stars_kb(lang))

@router.message(BookingStates.hotel)
async def state_hotel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
    
    text = message.text
    if text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "btn_other"), reply_markup=cancel_reply_kb(lang))
        return

    await state.update_data(hotel=text)
    await state.set_state(BookingStates.meals)
    await message.answer(get_text(lang, "action_meals"), reply_markup=meals_kb(lang))

@router.message(BookingStates.meals)
async def state_meals(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu_kb(lang))
        return
    
    text = message.text
    if text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "btn_other"), reply_markup=cancel_reply_kb(lang))
        return

    await state.update_data(meals=text)
    
    # Calculate
    pax = data['pax']
    base_price = pax * 150
    prices = [base_price, int(base_price * 1.4), int(base_price * 2.2)]
    await state.update_data(prices=prices)
    
    summary = (
        f"{get_text(lang, 'summary_title')}\n"
        f"{data['origin']} -> {data['dest']}\n"
        f"{data['date_out']} - {data['date_ret']}\n"
        f"{data['pax']} pax, {data['hotel']}, {text}"
    )
    await message.answer(summary, reply_markup=main_menu_kb(lang))
    await message.answer(get_text(lang, "select_tariff"), reply_markup=tariffs_inline_kb(lang, prices))
    await state.set_state(BookingStates.tariff)

@router.callback_query(BookingStates.tariff)
async def cb_tariff(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    idx = int(call.data.split("_")[1])
    
    prices = data['prices']
    price = prices[idx]
    names = ["Economy", "Standard", "Comfort"]
    fare_name = names[idx]
    
    save_data = {
        "user_id": call.from_user.id,
        "from_city": data['origin'],
        "to_city": data['dest'],
        "depart_date": data['date_out'],
        "return_date": data['date_ret'],
        "budget_value": data['budget_val'],
        "budget_currency": data['budget_curr'],
        "passengers": data['pax'],
        "hotel": data['hotel'],
        "meals": data['meals'],
        "fare_name": fare_name,
        "price_value": price,
        "price_currency": "USD",
        "status": "pending"
    }
    
    booking_id = await bookings_repo.create_booking(save_data)
    await call.message.delete()
    await call.message.answer(get_text(lang, "booking_created").format(booking_id), reply_markup=payment_inline_kb(lang, booking_id))
    await state.clear()

@router.callback_query(F.data.startswith("pay_"))
async def cb_pay(call: types.CallbackQuery):
    user = await users_repo.get_user(call.from_user.id)
    lang = user[3]
    book_id = int(call.data.split("_")[1])
    
    await bookings_repo.update_status(book_id, "paid")
    await call.message.edit_text(get_text(lang, "pay_success").format(book_id))

@router.message(F.text.in_(["Мои заявки", "Mening buyurtmalarim"]))
async def cmd_history(message: types.Message):
    user = await users_repo.get_user(message.from_user.id)
    lang = user[3]
    await show_history_page(message.from_user.id, lang, message, 0)

@router.callback_query(F.data.startswith("hist_"))
async def cb_history(call: types.CallbackQuery):
    user = await users_repo.get_user(call.from_user.id)
    lang = user[3]
    offset = int(call.data.split("_")[1])
    await call.message.delete()
    await show_history_page(call.from_user.id, lang, call.message, offset)

async def show_history_page(user_id, lang, message, offset):
    limit = 5
    items = await bookings_repo.get_by_user(user_id, limit, offset)
    if not items and offset == 0:
        await message.answer(get_text(lang, "history_empty"))
        return
    
    # We need total count for proper pagination logic in real app, but here we simply checks if we got 5
    # Simplification: if len(items) == limit, show next
    
    text = f"{get_text(lang, 'history_title')}\n\n"
    for item in items:
        status_key = f"status_{item['status']}"
        status_txt = get_text(lang, status_key)
        text += (
            f"🎫 #{item['id']} | {item['created_at'][:16]}\n"
            f"✈️ {item['from_city']} -> {item['to_city']}\n"
            f"📅 {item['depart_date']} - {item['return_date']}\n"
            f"💵 {item['price_value']} {item['price_currency']} ({item['fare_name']})\n"
            f"STATUS: {status_txt}\n\n"
        )
        
    # Hacky total estimation for "next" button
    total = offset + limit + 1 if len(items) == limit else offset + len(items)
    
    await message.answer(text, reply_markup=history_paging_kb(lang, offset, limit, total))
