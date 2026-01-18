from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.reply import selection_countries, selection_dates, selection_people, contact_share_keyboard, main_menu
from bot.db.repositories.requests_repo import RequestsRepository

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
    await message.answer("Куда хотите полететь?", reply_markup=selection_countries())

@router.message(SelectionFSM.choosing_country)
async def chosen_country(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Отменено", reply_markup=main_menu())
        return
    await state.update_data(country=message.text)
    await state.set_state(SelectionFSM.choosing_date)
    await message.answer("Когда планируете?", reply_markup=selection_dates())

@router.message(SelectionFSM.choosing_date)
async def chosen_date(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Отменено", reply_markup=main_menu())
        return
    await state.update_data(travel_month=message.text)
    await state.set_state(SelectionFSM.entering_budget)
    await message.answer("Ваш бюджет на человека (в USD)?", reply_markup=types.ReplyKeyboardRemove())

@router.message(SelectionFSM.entering_budget)
async def entered_budget(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число (USD).")
        return
    await state.update_data(budget_value=int(message.text), budget_currency="USD")
    await state.set_state(SelectionFSM.choosing_people)
    await message.answer("Сколько человек?", reply_markup=selection_people())

@router.message(SelectionFSM.choosing_people)
async def chosen_people(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Отменено", reply_markup=main_menu())
        return
    
    count = 4 if message.text == "4+" else int(message.text)
    await state.update_data(people_count=count)
    await state.set_state(SelectionFSM.entering_preferences)
    await message.answer("Ваши пожелания (отель, питание)?", reply_markup=types.ReplyKeyboardRemove())

@router.message(SelectionFSM.entering_preferences)
async def entered_preferences(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data.update({
        "user_id": message.from_user.id,
        "request_type": "selection",
        "preferences": message.text
    })
    
    await requests_repo.create_request(data)
    await state.clear()
    await message.answer("Заявка принята! Менеджер свяжется с вами.", reply_markup=main_menu())

@router.callback_query(F.data.startswith("apply_"))
async def start_tour_application(call: types.CallbackQuery, state: FSMContext):
    tour_id = int(call.data.split("_")[1])
    await state.update_data(tour_id=tour_id, request_type="tour")
    await state.set_state(ApplicationFSM.entering_contact)
    await call.message.answer("Пожалуйста, отправьте ваш номер телефона", reply_markup=contact_share_keyboard())
    await call.answer()

@router.message(ApplicationFSM.entering_contact)
async def entered_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    await state.set_state(ApplicationFSM.entering_method)
    await message.answer("Как с вами связаться? (Напишите: Telegram / Звонок)", reply_markup=types.ReplyKeyboardRemove())

@router.message(ApplicationFSM.entering_method)
async def entered_method(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data.update({
        "user_id": message.from_user.id,
        "contact_method": message.text
    })
    await requests_repo.create_request(data)
    await state.clear()
    await message.answer("Заявка на тур оформлена!", reply_markup=main_menu())
