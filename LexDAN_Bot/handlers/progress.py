from aiogram import Router, types
from aiogram.filters import Command
from handlers.keyboards import profile_menu
from services.database import load_users, get_user

router = Router()

# --- ОБРАБОТЧИК КНОПКИ "ПРОФИЛЬ" ---
@router.message(lambda m: m.text == "📊 Профиль")
async def profile_handler(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    
    # Данные пользователя
    name = user.get("name", "Не указано")
    lessons_done = user.get("lessons_done", 0)
    words_learned = user.get("words_learned", 0)
    level = user.get("level", "A1")
    
    # Статус подписки
    premium_until = user.get("premium_until", 0)
    import time
    if time.time() < premium_until:
        subscription = "Золото"  # позже добавим логику для Бриллианта
    else:
        subscription = "Серебро"
    
    profile_text = (
        f"📊 *Твой профиль:*\n\n"
        f"📛 Имя: {name}\n"
        f"📚 Пройдено уроков: {lessons_done}\n"
        f"📈 Уровень: {level}\n"
        f"📝 Слов выучено: {words_learned}\n"
        f"💎 Подписка: {subscription}"
    )
    
    await m.reply(profile_text, parse_mode="Markdown", reply_markup=profile_menu())