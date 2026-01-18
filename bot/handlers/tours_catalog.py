from aiogram import Router, types, F
from bot.db.repositories.tours_repo import ToursRepository
from bot.db.repositories.users_repo import UsersRepository
from bot.keyboards.inline import tour_actions, paging_keyboard
from bot.texts.localization import get_text, get_all_variants

router = Router()
tours_repo = ToursRepository()
user_repo = UsersRepository()

@router.message(F.text.in_(get_all_variants("btn_catalog").union(get_all_variants("btn_hot_tours"))))
async def show_catalog(message: types.Message):
    user = await user_repo.get_user(message.from_user.id)
    lang = user[3] if user and len(user) > 3 else "ru"
    
    is_hot = message.text in get_all_variants("btn_hot_tours")
    limit = 1
    offset = 0
    
    tours = await tours_repo.get_all_active(offset=offset, limit=limit, hot_only=is_hot)
    total = 10 
    
    if not tours:
        await message.answer(get_text(lang, "no_tours"))
        return

    tour = tours[0]
    text = format_tour(tour)
    
    kb = tour_actions(tour["tour_id"], lang)
    
    if tour["image_url"]:
        await message.answer_photo(
            photo=tour["image_url"],
            caption=text,
            reply_markup=kb
        )
    else:
        await message.answer(text, reply_markup=kb)

@router.inline_query(F.query.startswith("tour_"))
async def share_tour_inline(query: types.InlineQuery):
    tour_id = int(query.query.split("_")[1])
    tour = await tours_repo.get_by_id(tour_id)
    
    if not tour:
        return
        
    text = format_tour(tour)
    result = types.InlineQueryResultArticle(
        id=str(tour_id),
        title=tour["title"],
        description=f"{tour['country']} - {tour['price_from']}",
        thumb_url=tour["image_url"],
        input_message_content=types.InputTextMessageContent(message_text=text)
    )
    await query.answer([result], is_personal=True)

def format_tour(tour):
    hot_text = "HOT! " if tour["hot"] else ""
    return (
        f"{hot_text}**{tour['title']}**\n"
        f"📍 {tour['country']}, {tour['city']}\n"
        f"📅 {tour['duration_days']} Days | ⭐ {tour['hotel_stars']}\n"
        f"💰 From {tour['price_from']} {tour['currency']}\n\n"
        f"{tour['description']}\n\n"
        f"✅ {tour['included']}"
    )
