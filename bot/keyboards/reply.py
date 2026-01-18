from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton
from bot.texts.localization import get_text

def lang_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Русский", callback_data="setlang_ru")
    builder.button(text="O'zbekcha", callback_data="setlang_uz")
    return builder.as_markup()

def main_menu_kb(lang):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=get_text(lang, "btn_book")), KeyboardButton(text=get_text(lang, "btn_my_requests")))
    builder.row(KeyboardButton(text=get_text(lang, "btn_lang")), KeyboardButton(text=get_text(lang, "btn_contacts")))
    builder.row(KeyboardButton(text=get_text(lang, "btn_help")))
    return builder.as_markup(resize_keyboard=True)

def cancel_reply_kb(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_text(lang, "btn_cancel"))
    return builder.as_markup(resize_keyboard=True)

def cities_kb(lang, exclude=None):
    builder = ReplyKeyboardBuilder()
    ru_cities = ["Ташкент", "Москва", "Дубай", "Стамбул", "Самарканд", "Бухара"]
    uz_cities = ["Toshkent", "Moskva", "Dubay", "Istanbul", "Samarqand", "Buxoro"]
    cities = ru_cities if lang == "ru" else uz_cities
    
    for c in cities:
        if exclude and c == exclude:
            continue
        builder.button(text=c)
    builder.button(text=get_text(lang, "btn_other"))
    builder.button(text=get_text(lang, "btn_cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def currency_kb(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text="USD")
    builder.button(text="UZS")
    builder.button(text=get_text(lang, "btn_cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def pax_kb(lang):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 7):
        builder.button(text=str(i))
    builder.button(text=get_text(lang, "btn_other"))
    builder.button(text=get_text(lang, "btn_cancel"))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def hotel_stars_kb(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text="3*")
    builder.button(text="4*")
    builder.button(text="5*")
    builder.button(text=get_text(lang, "btn_other"))
    builder.button(text=get_text(lang, "btn_cancel"))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def meals_kb(lang):
    builder = ReplyKeyboardBuilder()
    opts = ["Breakfast", "Half board", "All inclusive"]
    for o in opts:
        builder.button(text=o)
    builder.button(text=get_text(lang, "btn_other"))
    builder.button(text=get_text(lang, "btn_cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def tariffs_inline_kb(lang, prices):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{get_text(lang, 'tariff_eco')} - {prices[0]} USD", callback_data="tariff_0")
    builder.button(text=f"{get_text(lang, 'tariff_std')} - {prices[1]} USD", callback_data="tariff_1")
    builder.button(text=f"{get_text(lang, 'tariff_com')} - {prices[2]} USD", callback_data="tariff_2")
    builder.adjust(1)
    return builder.as_markup()

def payment_inline_kb(lang, booking_id):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(lang, "btn_pay"), callback_data=f"pay_{booking_id}")
    return builder.as_markup()

def history_paging_kb(lang, offset, limit, total):
    builder = InlineKeyboardBuilder()
    if offset > 0:
        builder.button(text=get_text(lang, "btn_prev"), callback_data=f"hist_{offset-limit}")
    if offset + limit < total:
        builder.button(text=get_text(lang, "btn_next"), callback_data=f"hist_{offset+limit}")
    return builder.as_markup()

def request_details_kb(lang, booking_id):
    pass
