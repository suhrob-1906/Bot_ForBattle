from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.reply import main_menu, cities_keyboard, simple_options_keyboard
from bot.db.repositories.tickets_repo import TicketsRepository
from bot.db.repositories.users_repo import UsersRepository
from bot.texts.localization import get_text, get_all_variants
from bot.keyboards.inline import payment_confirm 
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
tickets_repo = TicketsRepository()
user_repo = UsersRepository()

class TicketFSM(StatesGroup):
    origin = State()
    destination = State()
    date = State()
    confirm = State()

@router.message(F.text.in_(get_all_variants("btn_flight_tickets")))
async def start_tickets(message: types.Message, state: FSMContext):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user else "ru"
    await state.update_data(lang=lang)
    
    await state.set_state(TicketFSM.origin)
    await message.answer(get_text(lang, "Action_Select_Origin"), reply_markup=cities_keyboard(lang))

@router.message(TicketFSM.origin)
async def ticket_origin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    await state.update_data(origin=message.text)
    await state.set_state(TicketFSM.destination)
    await message.answer(get_text(lang, "Action_Select_Destination"), reply_markup=cities_keyboard(lang))

@router.message(TicketFSM.destination)
async def ticket_dest(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text in get_all_variants("Btn_Cancel"):
        await state.clear()
        await message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
        return

    await state.update_data(destination=message.text)
    await state.set_state(TicketFSM.date)
    await message.answer(get_text(lang, "Action_Enter_Date_OneWay"), reply_markup=types.ReplyKeyboardRemove())

@router.message(TicketFSM.date)
async def ticket_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    origin = data.get("origin")
    dest = data.get("destination")
    date_val = message.text
    
    price = 450 if "NewYork" in dest else 150
    currency = "USD"
    
    await state.update_data(flight_date=date_val, price=price, currency=currency)
    
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text(lang, "Btn_Confirm_Book"), callback_data="book_ticket_confirm")
    kb.button(text=get_text(lang, "Btn_Cancel"), callback_data="book_ticket_cancel")
    
    text = get_text(lang, "Action_Ticket_Found").format(origin, dest, date_val, price, currency)
    await state.set_state(TicketFSM.confirm)
    await message.answer(text, reply_markup=kb.as_markup())

@router.callback_query(TicketFSM.confirm, F.data == "book_ticket_confirm")
async def ticket_confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    user = await user_repo.get_user(call.from_user.id)
    
    await tickets_repo.create_ticket(
        call.from_user.id, 
        data["origin"], data["destination"], 
        data["flight_date"], data["price"], data["currency"]
    )
    
    msg = get_text(lang, "Msg_Ticket_Booked").format(
        user[2], # Full Name
        data["origin"], data["destination"],
        data["price"], data["currency"]
    )
    
    await state.clear()
    await call.message.delete()
    await call.message.answer(msg, reply_markup=main_menu(lang))
    await call.answer()

@router.callback_query(TicketFSM.confirm, F.data == "book_ticket_cancel")
async def ticket_cancel_action(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.clear()
    await call.message.delete()
    await call.message.answer(get_text(lang, "main_menu"), reply_markup=main_menu(lang))
