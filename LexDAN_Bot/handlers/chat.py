from aiogram import Router, types
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu

router = Router()

# --- ХРАНИЛИЩЕ ПОСЛЕДНЕГО СООБЩЕНИЯ БОТА (ДЛЯ ПЕРЕВОДА) ---
user_last_message = {}

@router.message()
async def chat_handler(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # --- ШАГ 1: Пользователь пишет имя ---
    if user.get("step") == "awaiting_name":
        user["name"] = m.text.strip()
        user["step"] = "ready"
        save_users(users)

        welcome_text = (
            f"🎉 Привет, {user['name']}! Рад познакомиться!\n\n"
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
        return

    # --- ШАГ 2: Обработка кнопок (ReplyKeyboard) ---
    if m.text == "🗣️ Общаться":
        await m.reply(
            "🗣️ Отправь мне голосовое или текстовое сообщение на английском, "
            "я отвечу и переведу, если нужно.\n\n"
            "🔙 Чтобы вернуться — нажми кнопку ниже.",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📚 Уроки":
        await m.reply(
            "📚 Раздел «Уроки» сейчас в разработке.\n"
            "Скоро здесь появятся интерактивные занятия!\n"
            "Следи за обновлениями 🚀",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📊 Профиль":
        # Формируем профиль
        name = user.get("name", "Не указано")
        lessons_done = user.get("lessons_done", 0)
        words_learned = user.get("words_learned", 0)
        level = user.get("level", "A1")
        
        # Статус подписки
        premium_until = user.get("premium_until", 0)
        import time
        if time.time() < premium_until:
            # Проверяем, какая подписка (по умолчанию Золото)
            # Позже добавим логику для Бриллианта
            subscription = "Золото"
        else:
            subscription = "Серебро"

        profile_text = (
            f"📊 Твой профиль:\n\n"
            f"📛 Имя: {name}\n"
            f"📚 Пройдено уроков: {lessons_done}\n"
            f"📈 Уровень: {level}\n"
            f"📝 Слов выучено: {words_learned}\n"
            f"💎 Подписка: {subscription}"
        )
        await m.reply(profile_text, reply_markup=profile_menu())
        return

    if m.text == "🆘 Поддержка":
        await m.reply(
            "🆘 По всем вопросам работы бота, подписке и прочему — пиши сюда: @твой_ник"
        )
        return

    if m.text == "🔙 Вернуться в меню":
        await m.reply(
            "🏠 Ты в главном меню. Выбери, что хочешь делать.",
            reply_markup=main_menu()
        )
        return

    if m.text == "💎 Подписка":
        await m.reply(
            "💎 *Тарифы:*\n\n"
            "🆓 *Серебро* — бесплатно (20 голосовых/день)\n"
            "🥇 *Золото* — 399 ₽ (безлимит голосовые + текст)\n"
            "💎 *Бриллиант* — 799 ₽ (всё из Золота + уроки)\n\n"
            "Чтобы купить, напиши в поддержку: @твой_ник",
            parse_mode="Markdown"
        )
        return

    # --- ШАГ 3: Если пользователь пишет текст без кнопки ---
    if m.text and not m.text.startswith('/'):
        await m.reply(
            "Пожалуйста, выбери действие с помощью кнопок ниже.\n"
            "Если хочешь пообщаться — нажми «🗣️ Общаться».\n"
            "Если хочешь учиться — нажми «📚 Уроки».\n"
            "Если хочешь посмотреть свой прогресс — открой «📊 Профиль».\n"
            "Если возникли вопросы — жми «🆘 Поддержка».",
            reply_markup=main_menu()
        )
        return

    # --- ШАГ 4: Голосовые сообщения (пока заглушка) ---
    if m.voice:
        await m.reply(
            "🎧 Голосовые сообщения пока в разработке.\n"
            "Скоро я научусь их распознавать и отвечать голосом! 🚀",
            reply_markup=back_to_menu()
        )
        return