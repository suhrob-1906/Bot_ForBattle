from aiogram.utils.keyboard import InlineKeyboardBuilder

def tour_actions(tour_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Оставить заявку", callback_data=f"apply_{tour_id}")
    return builder.as_markup()

def paging_keyboard(offset, limit, total, prefix="catalog"):
    builder = InlineKeyboardBuilder()
    if offset > 0:
        builder.button(text="Назад", callback_data=f"{prefix}_page_{offset - limit}")
    if offset + limit < total:
        builder.button(text="Вперед", callback_data=f"{prefix}_page_{offset + limit}")
    return builder.as_markup()

def request_actions(request_id, status, has_payment=False):
    builder = InlineKeyboardBuilder()
    if status in ["new", "in_progress"]:
        builder.button(text="Отменить", callback_data=f"cancel_req_{request_id}")
    if not has_payment and status != "canceled":
        builder.button(text="Фейковая бронь", callback_data=f"pay_req_{request_id}")
    return builder.as_markup()

def payment_confirm(payment_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить оплату (Тест)", callback_data=f"confirm_pay_{payment_id}")
    return builder.as_markup()
