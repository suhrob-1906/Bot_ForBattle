from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton
from bot.texts.localization import get_text

def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Русский", callback_data="lang_ru")
    builder.button(text="O'zbekcha", callback_data="lang_uz")
    return builder.as_markup()

def main_menu(lang="ru"):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=get_text(lang, "btn_select_tour")),
        KeyboardButton(text=get_text(lang, "btn_flight_tickets"))
    )
    builder.row(
        KeyboardButton(text=get_text(lang, "btn_hot_tours")),
        KeyboardButton(text=get_text(lang, "btn_catalog"))
    )
    builder.row(
        KeyboardButton(text=get_text(lang, "btn_my_requests")),
        KeyboardButton(text=get_text(lang, "btn_contacts"))
    )
    return builder.as_markup(resize_keyboard=True)

def cities_keyboard(lang="ru"):
    builder = ReplyKeyboardBuilder()
    cities = ["City_Tashkent", "City_Moscow", "City_Dubai", "City_Istanbul", "City_Samarkand", "City_NewYork"]
    for city_key in cities:
        builder.button(text=get_text(lang, city_key))
    builder.button(text=get_text(lang, "Btn_Other_City"))
    builder.button(text=get_text(lang, "Btn_Cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def contact_share_keyboard(lang="ru"):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Send Contact", request_contact=True)
    builder.button(text=get_text(lang, "Btn_Cancel"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Reusing simplified builders for other inputs, ensuring they accept lang argument
def simple_options_keyboard(options, lang="ru"):
    builder = ReplyKeyboardBuilder()
    for opt in options:
        builder.button(text=opt)
    builder.button(text=get_text(lang, "Btn_Cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
