from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.db.repositories.users_repo import UsersRepository
from bot.db.repositories.tours_repo import BookingsRepository
from bot.keyboards.reply import cities_opts, cancel_kb, currency_opts, pax_opts, hotel_opts, meals_opts, fare_kb, pay_kb, main_menu
from bot.texts.localization import get_text
import re

router = Router()
user_repo = UsersRepository()
booking_repo = BookingsRepository()

class BookingFSM(StatesGroup):
    origin = State()
    destination = State()
    dates = State()
    budget = State()
    passengers = State()
    hotel = State()
    meals = State()
    fare = State()
    payment = State()

@router.message(F.text.in_(["Оформить билет", "Chipta rasmiylashtirish"]))
async def start_booking(message: types.Message, state: FSMContext):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3]
    await state.update_data(lang=lang)
    await state.set_state(BookingFSM.origin)
    await message.answer(get_text(lang, "city_origin"), reply_markup=cities_opts(lang))

@router.message(BookingFSM.origin)
async def process_origin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    text = message.text
    if text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "enter_city"), reply_markup=cancel_kb(lang))
        return

    await state.update_data(from_city=text)
    await state.set_state(BookingFSM.destination)
    await message.answer(get_text(lang, "city_dest"), reply_markup=cities_opts(lang, exclude=text))

@router.message(BookingFSM.destination)
async def process_dest(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    text = message.text
    if text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "enter_city"), reply_markup=cancel_kb(lang))
        return

    await state.update_data(to_city=text)
    await state.set_state(BookingFSM.dates)
    await message.answer(get_text(lang, "enter_dates"), reply_markup=cancel_kb(lang))

@router.message(BookingFSM.dates)
async def process_dates(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    pattern = r"\d{2}\.\d{2}\.\d{4}\s*-\s*\d{2}\.\d{2}\.\d{4}"
    if not re.match(pattern, message.text):
        await message.answer(get_text(lang, "err_dates"))
        return

    parts = message.text.split("-")
    await state.update_data(depart=parts[0].strip(), return_date=parts[1].strip())
    await state.set_state(BookingFSM.budget)
    await message.answer(get_text(lang, "enter_budget"), reply_markup=cancel_kb(lang))

@router.message(BookingFSM.budget)
async def process_budget(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    if not message.text.isdigit():
         await message.answer("Number please")
         return
         
    await state.update_data(budget=int(message.text))
    await message.answer(get_text(lang, "select_currency"), reply_markup=currency_opts(lang))

@router.message(F.text.in_(["USD", "UZS"]))
async def process_currency(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    # We catch the currency after budget input state, but we need to verify we are IN budget step or similar. 
    # Simplified: Assuming sequential flow.
    curr_state = await state.get_state()
    if curr_state == BookingFSM.budget:
        await state.update_data(currency=message.text)
        await state.set_state(BookingFSM.passengers)
        await message.answer(get_text(lang, "select_pax"), reply_markup=pax_opts(lang))

@router.message(BookingFSM.passengers)
async def process_pax(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    if message.text in ["Другое", "Boshqa"]:
        await message.answer(get_text(lang, "enter_pax"), reply_markup=cancel_kb(lang))
        return

    if not message.text.isdigit():
         await message.answer("Number please")
         return

    await state.update_data(pax=int(message.text))
    await state.set_state(BookingFSM.hotel)
    await message.answer(get_text(lang, "select_hotel"), reply_markup=hotel_opts(lang))

@router.message(BookingFSM.hotel)
async def process_hotel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    text = message.text 
    if text in ["Другое", "Boshqa"]:
        await message.answer("Enter hotel preference:", reply_markup=cancel_kb(lang))
        return

    await state.update_data(hotel=text)
    await state.set_state(BookingFSM.meals)
    await message.answer(get_text(lang, "select_meals"), reply_markup=meals_opts(lang))

@router.message(BookingFSM.meals)
async def process_meals(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    if message.text in ["Отмена", "Bekor qilish"]:
        await state.clear()
        await message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
        return

    text = message.text 
    if text in ["Другое", "Boshqa"]:
        await message.answer("Enter meals preference:", reply_markup=cancel_kb(lang))
        return

    await state.update_data(meals=text)
    
    # Calculate Prices
    base = 100 * data['pax']
    prices = {
        "eco": base,
        "std": base * 1.5,
        "com": base * 2.5
    }
    await state.update_data(prices=prices)
    
    summary = get_text(lang, "offer_header").format(
        data['from_city'], data['to_city'], 
        f"{data['depart']} - {data['return_date']}", 
        data['pax'], data['hotel'], text
    )
    
    await state.set_state(BookingFSM.fare)
    await message.answer(summary)
    await message.answer(get_text(lang, "fare_select"), reply_markup=fare_kb(prices, lang))

@router.callback_query(BookingFSM.fare)
async def process_fare(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    prices = data['prices']
    
    fare_code = call.data.split("_")[1]
    price = prices[fare_code]
    fare_name = fare_code
    
    await state.update_data(price=price, fare=fare_name)
    
    # Save pending
    save_data = {
        "user_id": call.from_user.id,
        "from_city": data['from_city'],
        "to_city": data['to_city'],
        "depart_date": data['depart'],
        "return_date": data['return_date'],
        "budget_value": data['budget'],
        "budget_currency": data['currency'],
        "passengers": data['pax'],
        "hotel": data['hotel'],
        "meals": data['meals'],
        "price_value": price,
        "price_currency": "USD",
        "fare_name": fare_name,
        "status": "pending"
    }
    await booking_repo.create_booking(save_data)
    
    # In a real app we would get the ID back, but for now let's just show pay button
    # To get ID we need repo to return cursor.lastrowid
    
    await call.message.delete()
    await state.set_state(BookingFSM.payment)
    await call.message.answer(get_text(lang, "booked").format("NEW"), reply_markup=pay_kb(lang))
    await call.answer()

@router.callback_query(BookingFSM.payment, F.data == "pay_confirm")
async def process_pay(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    
    # Mark paid (logic usually requires updates last order)
    # Simplified
    await call.message.edit_text(get_text(lang, "paid_success"))
    await call.message.answer(get_text(lang, "menu"), reply_markup=main_menu(lang))
    await state.clear()
    await call.answer()
