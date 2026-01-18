from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.texts.localization import get_text

def tour_actions(tour_id, lang="ru"):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(lang, "inline_apply"), callback_data=f"apply_{tour_id}")
    builder.button(text=get_text(lang, "inline_share"), switch_inline_query=f"tour_{tour_id}")
    builder.adjust(1)
    return builder.as_markup()

def paging_keyboard(offset, limit, total, prefix="catalog", lang="ru"):
    builder = InlineKeyboardBuilder()
    if offset > 0:
        builder.button(text=get_text(lang, "inline_back"), callback_data=f"{prefix}_page_{offset - limit}")
    if offset + limit < total:
        builder.button(text=get_text(lang, "inline_forward"), callback_data=f"{prefix}_page_{offset + limit}")
    return builder.as_markup()

def request_actions(request_id, status, has_payment=False, lang="ru"):
    builder = InlineKeyboardBuilder()
    if status in ["new", "in_progress"]:
        builder.button(text=get_text(lang, "inline_cancel"), callback_data=f"cancel_req_{request_id}")
    if not has_payment and status != "canceled":
        builder.button(text=get_text(lang, "inline_pay"), callback_data=f"pay_req_{request_id}")
    return builder.as_markup()

def payment_confirm(payment_id, lang="ru"):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(lang, "inline_confirm_pay"), callback_data=f"confirm_pay_{payment_id}")
    return builder.as_markup()
