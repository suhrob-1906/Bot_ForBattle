from aiogram import Router, types, F
from bot.db.repositories.requests_repo import RequestsRepository
from bot.db.repositories.users_repo import UsersRepository
from bot.keyboards.inline import request_actions
from bot.texts.localization import get_all_variants

router = Router()
requests_repo = RequestsRepository()
user_repo = UsersRepository()

@router.message(F.text.in_(get_all_variants("btn_my_requests")))
async def my_requests(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user else "ru"

    reqs = await requests_repo.get_by_user(message.from_user.id)
    if not reqs:
        await message.answer("No active requests.")
        return

    for req in reqs:
        tour_info = f"Tour #{req['tour_id']}" if req['tour_id'] else "Selection"
        text = (
            f"ID {req['request_id']} | {req['status']}\n"
            f"Date: {req['created_at']}\n"
            f"Type: {tour_info}"
        )
        await message.answer(text, reply_markup=request_actions(req['request_id'], req['status'], lang=lang))

@router.callback_query(F.data.startswith("cancel_req_"))
async def cancel_request(call: types.CallbackQuery):
    req_id = int(call.data.split("_")[2])
    await requests_repo.cancel_request(req_id)
    await call.message.edit_text(call.message.text + "\nCANCELED")
    await call.answer()
