from aiogram import Router, types, F
from bot.db.repositories.tours_repo import ToursRepository
from bot.db.repositories.users_repo import UsersRepository
from bot.keyboards.inline import tour_actions
from bot.texts.localization import get_text

router = Router()
tours_repo = ToursRepository()
user_repo = UsersRepository()

@router.message(F.text.in_({"Каталог туров", "Горящие туры", "Turlar katalogi", "Qaynoq turlar"}))
async def show_catalog(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user and len(user) > 3 else "ru"
    
    is_hot = "Горящие" in message.text or "Qaynoq" in message.text
    tours = await tours_repo.get_all_active(offset=0, limit=1, hot_only=is_hot)
    
    if not tours:
        await message.answer(get_text(lang, "no_tours"))
        return

    tour = tours[0]
    text = format_tour(tour)
    
    if tour["image_url"]:
        await message.answer_photo(
            photo=tour["image_url"],
            caption=text,
            reply_markup=tour_actions(tour["tour_id"])
        )
    else:
        await message.answer(text, reply_markup=tour_actions(tour["tour_id"]))

def format_tour(tour):
    hot_text = "HOT! " if tour["hot"] else ""
    return (
        f"{hot_text}**{tour['title']}**\n"
        f"Страна: {tour['country']}, {tour['city']}\n"
        f"Дней: {tour['duration_days']} | Звезд: {tour['hotel_stars']}\n"
        f"Цена: От {tour['price_from']} {tour['currency']}\n\n"
        f"{tour['description']}\n\n"
        f"Включено: {tour['included']}"
    )
