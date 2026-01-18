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
        KeyboardButton(text=get_text(lang, "btn_hot_tours"))
    )
    builder.row(
        KeyboardButton(text=get_text(lang, "btn_catalog")),
        KeyboardButton(text=get_text(lang, "btn_my_requests"))
    )
    builder.row(
        KeyboardButton(text=get_text(lang, "btn_contacts")),
        KeyboardButton(text=get_text(lang, "btn_faq"))
    )
    return builder.as_markup(resize_keyboard=True)


def contact_share_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Contact / Номер", request_contact=True)
    builder.button(text="Skip / Пропустить")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def selection_countries():
    builder = ReplyKeyboardBuilder()
    for country in ["Turkey", "UAE", "Egypt", "Europe", "Uzbekistan", "Other"]:
        builder.button(text=country)
    builder.button(text="Cancel")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def selection_dates():
    builder = ReplyKeyboardBuilder()
    builder.button(text="This month")
    builder.button(text="Next month")
    builder.button(text="Manual input")
    builder.button(text="Cancel")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def selection_people():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 5):
        builder.button(text=str(i))
    builder.button(text="4+")
    builder.button(text="Cancel")
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)
