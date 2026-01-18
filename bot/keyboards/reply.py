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
    builder.button(text="Send Contact", request_contact=True)
    builder.button(text="Cancel", request_contact=False)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def selection_countries():
    builder = ReplyKeyboardBuilder()
    countries = ["Turkey", "UAE", "Egypt", "Thailand", "Maldives", "Europe", "Uzbekistan", "USA"]
    for country in countries:
        builder.button(text=country)
    builder.button(text="Other")
    builder.button(text="Cancel")
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def selection_dates():
    builder = ReplyKeyboardBuilder()
    options = ["This Month", "Next Month", "Spring", "Summer", "Autumn", "Winter", "Any Dates"]
    for opt in options:
        builder.button(text=opt)
    builder.button(text="Cancel")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def selection_budget():
    builder = ReplyKeyboardBuilder()
    options = ["Economy ($500-)", "Regular ($500-1500)", "Premium ($1500-3000)", "Luxury ($3000+)", "No Limit"]
    for opt in options:
        builder.button(text=opt)
    builder.button(text="Cancel")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def selection_people():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 11):
        builder.button(text=str(i))
    builder.button(text="10+")
    builder.button(text="Cancel")
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True)

def selection_preferences():
    builder = ReplyKeyboardBuilder()
    tags = ["All Inclusive", "Breakfast only", "Beach Front", "City Center", "Quiet", "Party", "Kids Friendly", "Honeymoon"]
    for tag in tags:
        builder.button(text=tag)
    builder.button(text="Skip")
    builder.button(text="Cancel")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
