from aiogram import Router, types
from aiogram.filters import Command
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu

router = Router()

# --- КОМАНДА /start ---
@router.message(Command("start"))
async def start_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # --- ЕСЛИ ПОЛЬЗОВАТЕЛЬ НОВЫЙ (НЕТ ИМЕНИ) ---
    if user.get("name") is None:
        await m.reply(
            "👋 Привет! Я — LD (LexDan), твой личный ИИ-репетитор.\n"
            "🚀 Помогу выучить английский быстрее и дешевле, чем с репетитором.\n"
            "😊 Давай познакомимся! Как тебя зовут?"
        )
        user["step"] = "awaiting_name"
        save_users(users)
        return

    # --- ЕСЛИ ПОЛЬЗОВАТЕЛЬ УЖЕ ЗАРЕГИСТРИРОВАН ---
    welcome_text = (
        f"🎉 Привет, {user['name']}! Рад снова тебя видеть!\n\n"
        "🧠 Вот что я умею:\n"
        "• 💬 Общаться на английском — я исправлю ошибки и подскажу, как сказать лучше.\n"
        "• 🎤 Распознавать голосовые сообщения и отвечать на них голосом.\n"
        "• 📚 Проводить короткие интерактивные уроки (5-7 минут) по твоему уровню.\n"
        "• 📊 Отслеживать твой прогресс — ты видишь, сколько слов выучил и уроков прошёл.\n\n"
        "🎯 Твоя цель: заниматься 15–20 минут в день.\n"
        "⏳ Через месяц ты заметишь результат.\n\n"
        "👇 Что означают кнопки:\n"
        "🗣️ Общаться — простое общение на английском с переводом и голосовыми сообщениями.\n"
        "📚 Уроки — изучай английский с помощью коротких интерактивных занятий.\n"
        "📊 Профиль — твой прогресс, уровень и статистика.\n"
        "🆘 Поддержка — если есть вопросы, жми на кнопку.\n\n"
        "👇 Выбери, с чего начнёшь:"
    )
    await m.reply(welcome_text, reply_markup=main_menu())