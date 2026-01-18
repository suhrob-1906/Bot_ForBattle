MESSAGES = {
    "ru": {
        "start_new": "Привет! Пожалуйста, выберите язык:",
        "menu": "Главное меню",
        "btn_tour": "Подобрать тур",
        "btn_my_requests": "Мои заявки",
        "btn_lang": "Языки",
        "btn_contacts": "Контакты",
        "btn_help": "Помощь",
        "contacts_text": "Телефон: +998901091288\nОбратиться за помощью к Сухробу",
        "help_text": "Бот для подбора туров.\nНажмите Подобрать тур, чтобы создать заявку.",
        "lang_select": "Выберите язык / Tilni tanlang:",
        "lang_saved": "Язык сохранен: Русский",
        
        "q_dest": "Куда хотите полететь?",
        "q_date": "Когда планируете?",
        "q_budget": "Ваш бюджет на человека (в USD)?",
        "q_pax": "Сколько человек?",
        "q_wishes": "Ваши пожелания (отель, питание)?",
        
        "err_number": "Пожалуйста, введите число (например 600).",
        "booking_created": "Заявка #{} принята! Мы скоро свяжемся с вами.",
        
        "history_title": "Мои заявки:",
        "history_empty": "У вас пока нет заявок.",
        "status_pending": "Ожидает",
        "status_paid": "Оплачено",
        "btn_cancel": "Отмена"
    },
    "uz": {
        "start_new": "Salom! Iltimos, tilni tanlang:",
        "menu": "Asosiy menyu",
        "btn_tour": "Tur tanlash",
        "btn_my_requests": "Mening buyurtmalarim",
        "btn_lang": "Tillar",
        "btn_contacts": "Aloqa",
        "btn_help": "Yordam",
        "contacts_text": "Telefon: +998901091288\nSuhrobga murojaat qiling",
        "help_text": "Tur tanlash boti.\nBuyurtma berish uchun Tur tanlash tugmasini bosing.",
        "lang_select": "Tilni tanlang / Выберите язык:",
        "lang_saved": "Til saqlandi: O'zbekcha",
        
        "q_dest": "Qayerga uchmoqchisiz?",
        "q_date": "Qachon rejalashtiryapsiz?",
        "q_budget": "Bir kishi uchun budjetingiz (USD)?",
        "q_pax": "Necha kishi?",
        "q_wishes": "Istaklaringiz (mehmonxona, ovqat)?",
        
        "err_number": "Iltimos, raqam kiriting (masalan 600).",
        "booking_created": "Buyurtma #{} qabul qilindi! Tez orada bog'lanamiz.",
        
        "history_title": "Mening buyurtmalarim:",
        "history_empty": "Sizda hozircha buyurtmalar yo'q.",
        "status_pending": "Kutilmoqda",
        "status_paid": "To'landi",
        "btn_cancel": "Bekor qilish"
    }
}

def get_text(lang, key):
    res = MESSAGES.get(lang)
    if not res:
        res = MESSAGES.get("ru")
    return res.get(key, key)
