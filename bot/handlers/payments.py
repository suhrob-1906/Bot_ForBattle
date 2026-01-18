from aiogram import Router, types, F
from bot.db.repositories.payments_repo import PaymentsRepository
from bot.db.repositories.requests_repo import RequestsRepository
from bot.keyboards.inline import payment_confirm

router = Router()
payments_repo = PaymentsRepository()
requests_repo = RequestsRepository()

@router.callback_query(F.data.startswith("pay_req_"))
async def initiate_payment(call: types.CallbackQuery):
    req_id = int(call.data.split("_")[2])
    request = await requests_repo.get_by_id(req_id)
    
    if not request:
        await call.answer("Заявка не найдена", show_alert=True)
        return

    amount = 50.0
    payment_id = await payments_repo.create_payment(req_id, call.from_user.id, amount, "USD")
    
    await call.message.answer(
        f"Фейковая оплата\n\nСумма: {amount} USD\nНазначение: Бронь по заявке #{req_id}",
        reply_markup=payment_confirm(payment_id)
    )
    await call.answer()

@router.callback_query(F.data.startswith("confirm_pay_"))
async def confirm_payment(call: types.CallbackQuery):
    payment_id = int(call.data.split("_")[2])
    payment = await payments_repo.get_by_id(payment_id)
    
    if not payment or payment['status'] == 'paid':
        await call.answer("Уже оплачено или ошибка", show_alert=True)
        return

    await payments_repo.mark_paid(payment_id)
    await requests_repo.update_status(payment['request_id'], "confirmed")
    
    await call.message.edit_text(call.message.text + "\n\nОПЛАЧЕНО (Тест)")
    await call.answer("Успешно!")
