from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.reply import selection_countries, selection_dates, selection_people, selection_budget, selection_preferences, contact_share_keyboard, main_menu
from bot.db.repositories.requests_repo import RequestsRepository
import re

router = Router()
requests_repo = RequestsRepository()

class SelectionFSM(StatesGroup):
    choosing_country = State()
    choosing_date = State()
    entering_budget = State()
    choosing_people = State()
    entering_preferences = State()
    completed = State()

class ApplicationFSM(StatesGroup):
    entering_contact = State()
    entering_method = State()

@router.message(F.text.in_({"Подобрать тур", "Tur tanlash"}))
async def start_selection(message: types.Message, state: FSMContext):
    await state.set_state(SelectionFSM.choosing_country)
    await message.answer("Choose destination:", reply_markup=selection_countries())

@router.message(SelectionFSM.choosing_country)
async def chosen_country(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Canceled", reply_markup=main_menu())
        return
    await state.update_data(country=message.text)
    await state.set_state(SelectionFSM.choosing_date)
    await message.answer("When do you plan to travel?", reply_markup=selection_dates())

@router.message(SelectionFSM.choosing_date)
async def chosen_date(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Canceled", reply_markup=main_menu())
        return
    await state.update_data(travel_month=message.text)
    await state.set_state(SelectionFSM.entering_budget)
    await message.answer("Select your budget range:", reply_markup=selection_budget())

@router.message(SelectionFSM.entering_budget)
async def entered_budget(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Canceled", reply_markup=main_menu())
        return
    await state.update_data(budget_value=message.text)
    await state.set_state(SelectionFSM.choosing_people)
    await message.answer("How many travelers?", reply_markup=selection_people())

@router.message(SelectionFSM.choosing_people)
async def chosen_people(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Canceled", reply_markup=main_menu())
        return
    
    await state.update_data(people_count=message.text)
    await state.set_state(SelectionFSM.entering_preferences)
    await message.answer("Any specific preferences?", reply_markup=selection_preferences())

@router.message(SelectionFSM.entering_preferences)
async def entered_preferences(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Canceled", reply_markup=main_menu())
        return

    data = await state.get_data()
    pref = message.text if message.text != "Skip" else "No preferences"
    
    data.update({
        "user_id": message.from_user.id,
        "request_type": "selection",
        "preferences": pref
    })
    
    await requests_repo.create_request(data)
    await state.clear()
    await message.answer("Request received! Our manager will contact you soon.", reply_markup=main_menu())

@router.callback_query(F.data.startswith("apply_"))
async def start_tour_application(call: types.CallbackQuery, state: FSMContext):
    tour_id = int(call.data.split("_")[1])
    await state.update_data(tour_id=tour_id, request_type="tour")
    await state.set_state(ApplicationFSM.entering_contact)
    await call.message.answer("Please share your phone number", reply_markup=contact_share_keyboard())
    await call.answer()

@router.message(ApplicationFSM.entering_contact)
async def entered_contact(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Canceled", reply_markup=main_menu())
        return

    phone = message.contact.phone_number if message.contact else message.text
    
    # Basic validation
    if not message.contact and not re.match(r"^\+?[\d\s-]{7,15}$", phone):
        await message.answer("Invalid phone format. Please try again or use the button.")
        return

    await state.update_data(phone=phone)
    await state.set_state(ApplicationFSM.entering_method)
    await message.answer("Preferred contact method? (Telegram/Call/Whatsapp)", reply_markup=types.ReplyKeyboardRemove())

@router.message(ApplicationFSM.entering_method)
async def entered_method(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data.update({
        "user_id": message.from_user.id,
        "contact_method": message.text
    })
    await requests_repo.create_request(data)
    await state.clear()
    await message.answer("Tour request submitted successfully!", reply_markup=main_menu())
