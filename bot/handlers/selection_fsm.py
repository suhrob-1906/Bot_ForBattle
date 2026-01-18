from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.reply import main_menu, cities_keyboard, simple_options_keyboard, contact_share_keyboard
from bot.db.repositories.requests_repo import RequestsRepository
from bot.texts.localization import get_text, get_all_variants
import re

router = Router()
requests_repo = RequestsRepository()

class SelectionFSM(StatesGroup):
    origin = State()
    destination = State()
    dates = State()
    budget = State()
    people = State()
    preferences = State()

class ApplicationFSM(StatesGroup):
    entering_contact = State()
    entering_method = State()

@router.message(F.text.in_(get_all_variants("btn_select_tour")))
async def start_selection(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # We need language here. A small hack since we don't have repo injected everywhere easily, 
    # but we can rely on what buttons the user pressed to infer lang or fetch from DB. 
    # For now, let's assume default RU if not found, usually middleware does this.
    # But consistent with other handlers, let's fetch or use 'ru'.
    # For simplicity in FSM, let's look at the button text they clicked.
    lang = "uz" if message.text == "Tur tanlash" else "ru"
    await state.update_data(lang=lang)
    
    await state.set_state(SelectionFSM.origin)
    await message.answer(get_text(lang, "Action_Select_Origin"), reply_markup=cities_keyboard(lang))

@router.message(SelectionFSM.origin)
async def fsm_origin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    await state.update_data(origin=message.text)
    await state.set_state(SelectionFSM.destination)
    await message.answer(get_text(lang, "Action_Select_Destination"), reply_markup=cities_keyboard(lang))

@router.message(SelectionFSM.destination)
async def fsm_destination(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    await state.update_data(destination=message.text)
    await state.set_state(SelectionFSM.dates)
    await message.answer(get_text(lang, "Action_Enter_Dates"), reply_markup=types.ReplyKeyboardRemove())

@router.message(SelectionFSM.dates)
async def fsm_dates(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    await state.update_data(travel_date=message.text) # storing full text like "10.05 - 20.05"
    await state.set_state(SelectionFSM.budget)
    
    opts = ["$500 - $1000", "$1000 - $2000", "$2000+", "No Limit"]
    await message.answer(get_text(lang, "Action_Select_Budget"), reply_markup=simple_options_keyboard(opts, lang))

@router.message(SelectionFSM.budget)
async def fsm_budget(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    await state.update_data(budget_value=message.text)
    await state.set_state(SelectionFSM.people)
    
    opts = ["1", "2", "3", "4+"]
    await message.answer(get_text(lang, "Action_Select_People"), reply_markup=simple_options_keyboard(opts, lang))

@router.message(SelectionFSM.people)
async def fsm_people(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    await state.update_data(people_count=message.text)
    await state.set_state(SelectionFSM.preferences)
    
    opts = ["All Inclusive", "Breakfast", "First Line", "City Hotel"]
    await message.answer(get_text(lang, "Action_Enter_Preferences"), reply_markup=simple_options_keyboard(opts, lang))

@router.message(SelectionFSM.preferences)
async def fsm_preferences(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return
        
    data.update({
        "user_id": message.from_user.id,
        "request_type": "selection",
        "preferences": message.text
    })
    
    # Clean data before saving (remove temp keys like 'lang')
    save_data = {k: v for k, v in data.items() if k != 'lang'}
    await requests_repo.create_request(save_data)
    
    await state.clear()
    await message.answer(get_text(lang, "req_status_new"), reply_markup=main_menu(lang))

# --- Tour Application Flow ---

@router.callback_query(F.data.startswith("apply_"))
async def start_tour_application(call: types.CallbackQuery, state: FSMContext):
    # Infer language or default
    lang = "ru" # Simplified, ideally fetch from DB
    await state.update_data(tour_id=int(call.data.split("_")[1]), request_type="tour", lang=lang)
    await state.set_state(ApplicationFSM.entering_contact)
    await call.message.answer(get_text(lang, "contacts_text"), reply_markup=contact_share_keyboard(lang))
    await call.answer()

@router.message(ApplicationFSM.entering_contact)
async def tour_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    await state.set_state(ApplicationFSM.entering_method)
    await message.answer("Telegram / WhatsApp / Call?", reply_markup=types.ReplyKeyboardRemove())

@router.message(ApplicationFSM.entering_method)
async def tour_method(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    data.update({
        "user_id": message.from_user.id,
        "contact_method": message.text
    })
    
    save_data = {k: v for k, v in data.items() if k != 'lang'}
    await requests_repo.create_request(save_data)
    
    await state.clear()
    await message.answer(get_text(lang, "req_status_new"), reply_markup=main_menu(lang))
