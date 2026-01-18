from aiogram import Router, types, F
from bot.db.repositories.requests_repo import RequestsRepository
from bot.keyboards.inline import request_actions

router = Router()
requests_repo = RequestsRepository()

@router.message(F.text.in_({"Мои заявки", "Mening arizalarim"}))
async def my_requests(message: types.Message):
    reqs = await requests_repo.get_by_user(message.from_user.id)
    if not reqs:
        await message.answer("У вас нет активных заявок.")
        return

    for req in reqs:
        tour_info = f"Тур #{req['tour_id']}" if req['tour_id'] else "Подбор тура"
        text = (
            f"Заявка {req['request_id']} | {req['status']}\n"
            f"Дата: {req['created_at']}\n"
            f"Тип: {tour_info}"
        )
        await message.answer(text, reply_markup=request_actions(req['request_id'], req['status']))

@router.callback_query(F.data.startswith("cancel_req_"))
async def cancel_request(call: types.CallbackQuery):
    req_id = int(call.data.split("_")[2])
    await requests_repo.cancel_request(req_id)
    await call.message.edit_text(call.message.text + "\nОТМЕНЕНО")
    await call.answer("Заявка отменена")
