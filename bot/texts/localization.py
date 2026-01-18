MESSAGES = {
    "ru": {
        "start": "Привет! Выберите язык / Tilni tanlang:",
        "main_menu": "Главное меню",
        "btn_select_tour": "Подобрать тур",
        "btn_hot_tours": "Горящие туры",
        "btn_catalog": "Каталог туров",
        "btn_my_requests": "Мои заявки",
        "btn_contacts": "Контакты",
        "btn_faq": "FAQ",
        "contacts_text": "Контакты\n\nТелефон: +998 90 123 45 67\nАдрес: Ташкент, Ц-1",
        "faq_text": "Частые вопросы\n\n1. Как забронировать? - Оставьте заявку.\n2. Где офис? - На Марсе.",
        "no_tours": "Туров пока нет",
        "req_status_new": "Новая",
        "req_status_in_progress": "В обработке",
        "req_status_confirmed": "Подтверждена",
        "req_status_canceled": "Отменена",
        "inline_apply": "📝 Оставить заявку",
        "inline_share": "🔗 Поделиться",
        "inline_back": "⬅️ Назад",
        "inline_forward": "Вперед ➡️",
        "inline_cancel": "❌ Отменить",
        "inline_pay": "💳 Фейковая бронь",
        "inline_confirm_pay": "✅ Подтвердить оплату (Тест)",
    },
    "uz": {
        "start": "Salom! Tilni tanlang / Выберите язык:",
        "main_menu": "Asosiy menyu",
        "btn_select_tour": "Tur tanlash",
        "btn_hot_tours": "Qaynoq turlar",
        "btn_catalog": "Turlar katalogi",
        "btn_my_requests": "Mening arizalarim",
        "btn_contacts": "Kontaktlar",
        "btn_faq": "FAQ",
        "contacts_text": "Kontaktlar\n\nTelefon: +998 90 123 45 67\nManzil: Toshkent, C-1",
        "faq_text": "Tez-tez so'raladigan savollar\n\n1. Qanday band qilish kerak? - Ariza qoldiring.\n2. Ofis qayerda? - Marsda.",
        "no_tours": "Turlar hozircha yo'q",
        "req_status_new": "Yangi",
        "req_status_in_progress": "Jarayonda",
        "req_status_confirmed": "Tasdiqlangan",
        "req_status_canceled": "Bekor qilingan",
        "inline_apply": "📝 Ariza qoldirish",
        "inline_share": "🔗 Ulashish",
        "inline_back": "⬅️ Orqaga",
        "inline_forward": "Oldinga ➡️",
        "inline_cancel": "❌ Bekor qilish",
        "inline_pay": "💳 Soxta bandlov",
        "inline_confirm_pay": "✅ To'lovni tasdiqlash (Test)",
    }
}

def get_text(lang_code, key):
    return MESSAGES.get(lang_code, MESSAGES["ru"]).get(key, key)

def get_all_variants(key):
    """Returns a set of all translations for a given key to use in filters"""
    return {lang_data.get(key, key) for lang_data in MESSAGES.values()}
