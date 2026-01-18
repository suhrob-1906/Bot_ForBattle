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
    builder.row(KeyboardButton(text=get_text(lang, "btn_tour")), KeyboardButton(text=get_text(lang, "btn_my_requests")))
    builder.row(KeyboardButton(text=get_text(lang, "btn_lang")), KeyboardButton(text=get_text(lang, "btn_contacts")))
    return builder.as_markup(resize_keyboard=True)

def cancel_reply_kb(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_text(lang, "btn_cancel"))
    return builder.as_markup(resize_keyboard=True)

def history_paging_kb(lang, offset, limit, total):
    builder = InlineKeyboardBuilder()
    if offset > 0:
        builder.button(text="<<", callback_data=f"hist_{offset-limit}")
    if offset + limit < total:
        builder.button(text=">>", callback_data=f"hist_{offset+limit}")
    return builder.as_markup()
