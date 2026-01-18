from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton
from bot.texts.localization import get_text

def lang_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    return builder.as_markup()

def main_menu(lang):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=get_text(lang, "btn_book")))
    builder.row(KeyboardButton(text=get_text(lang, "btn_hot")))
    builder.row(KeyboardButton(text=get_text(lang, "btn_history")))
    builder.row(KeyboardButton(text=get_text(lang, "btn_lang")))
    return builder.as_markup(resize_keyboard=True)

def cities_opts(lang, exclude=None):
    builder = ReplyKeyboardBuilder()
    cities_ru = ["Ташкент", "Самарканд", "Бухара", "Хива", "Фергана", "Наманган", "Алматы", "Бишкек", "Дубай", "Стамбул", "Анталья", "Москва"]
    cities_uz = ["Toshkent", "Samarqand", "Buxoro", "Xiva", "Farg'ona", "Namangan", "Olmaota", "Bishkek", "Dubay", "Istanbul", "Antaliya", "Moskva"]
    
    cities = cities_ru if lang == "ru" else cities_uz
    for city in cities:
        if exclude and city == exclude:
            continue
        builder.button(text=city)
        
    builder.button(text=get_text(lang, "other"))
    builder.button(text=get_text(lang, "cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def cancel_kb(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_text(lang, "cancel"))
    return builder.as_markup(resize_keyboard=True)

def currency_opts(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text="USD")
    builder.button(text="UZS")
    builder.button(text=get_text(lang, "cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def pax_opts(lang):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 7):
        builder.button(text=str(i))
    builder.button(text=get_text(lang, "other"))
    builder.button(text=get_text(lang, "cancel"))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def hotel_opts(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text="3*")
    builder.button(text="4*")
    builder.button(text="5*")
    builder.button(text=get_text(lang, "other"))
    builder.button(text=get_text(lang, "cancel"))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def meals_opts(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Breakfast")
    builder.button(text="Half board")
    builder.button(text="All inclusive")
    builder.button(text=get_text(lang, "other"))
    builder.button(text=get_text(lang, "cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
    
def fare_kb(prices, lang):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{get_text(lang, 'fare_eco')} - {prices['eco']}", callback_data="fare_eco")
    builder.button(text=f"{get_text(lang, 'fare_std')} - {prices['std']}", callback_data="fare_std")
    builder.button(text=f"{get_text(lang, 'fare_com')} - {prices['com']}", callback_data="fare_com")
    builder.adjust(1)
    return builder.as_markup()

def pay_kb(lang):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(lang, "pay_confirm"), callback_data="pay_confirm")
    return builder.as_markup()

def hot_nav_kb(offer_id, total_count, lang):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(lang, "prev"), callback_data=f"hot_prev_{offer_id}")
    builder.button(text=get_text(lang, "book_this"), callback_data=f"hot_book_{offer_id}")
    builder.button(text=get_text(lang, "next"), callback_data=f"hot_next_{offer_id}")
    builder.adjust(3)
    return builder.as_markup()

def history_nav_kb(offset, limit, total, lang):
    builder = InlineKeyboardBuilder()
    if offset > 0:
        builder.button(text=get_text(lang, "prev"), callback_data=f"hist_prev_{offset}")
    if offset + limit < total:
        builder.button(text=get_text(lang, "next"), callback_data=f"hist_next_{offset}")
    return builder.as_markup()
