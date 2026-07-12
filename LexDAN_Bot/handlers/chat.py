from aiogram import Router, types
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu, back_to_menu, profile_menu
import logging

router = Router()

# --- ХРАНИЛИЩЕ СОСТОЯНИЙ ПОЛЬЗОВАТЕЛЕЙ ---
user_states = {}  # user_id: "chat" / "profile" / "lessons" / "menu"

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

    # --- ШАГ 2: Обработка кнопок (если пользователь в меню) ---
    current_state = user_states.get(user_id, "menu")

    # --- Если пользователь НЕ в меню, то кнопки не работают (кроме "Вернуться") ---
    if current_state != "menu" and m.text != "🔙 Вернуться в меню":
        await m.reply(
            f"📍 Ты сейчас в разделе «{current_state}». Нажми «🔙 Вернуться в меню», чтобы перейти в главное меню."
        )
        return

    # --- ОБРАБОТКА КНОПОК (только если в меню) ---
    if m.text == "🗣️ Общаться":
        user_states[user_id] = "chat"
        await m.reply(
            "🗣️ Отправь мне голосовое или текстовое сообщение на английском, "
            "я отвечу и переведу, если нужно.\n\n"
            "🔙 Чтобы вернуться — нажми кнопку ниже.",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📚 Уроки":
        user_states[user_id] = "lessons"
        await m.reply(
            "📚 Раздел «Уроки» сейчас в разработке.\n"
            "Скоро здесь появятся интерактивные занятия!\n"
            "Следи за обновлениями 🚀",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📊 Профиль":
        user_states[user_id] = "profile"
        name = user.get("name", "Не указано")
        lessons_done = user.get("lessons_done", 0)
        words_learned = user.get("words_learned", 0)
        level = user.get("level", "A1")
        
        import time
        premium_until = user.get("premium_until", 0)
        if time.time() < premium_until:
            subscription = "Золото"
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
        return

    if m.text == "🆘 Поддержка":
        # Поддержка не меняет состояние
        await m.reply(
            "🆘 По всем вопросам работы бота, подписке и прочему — пиши сюда: @твой_ник"
        )
        return

    if m.text == "🔙 Вернуться в меню":
        user_states[user_id] = "menu"
        await m.reply(
            "🏠 Ты в главном меню. Выбери, что хочешь делать.",
            reply_markup=main_menu()
        )
        return

    if m.text == "💎 Подписка":
        # Подписка доступна только из профиля, но если кто-то напишет — покажем
        await m.reply(
            "💎 *Тарифы:*\n\n"
            "🆓 *Серебро* — бесплатно (20 голосовых/день)\n"
            "🥇 *Золото* — 399 ₽ (безлимит голосовые + текст)\n"
            "💎 *Бриллиант* — 799 ₽ (всё из Золота + уроки)\n\n"
            "Чтобы купить, напиши в поддержку: @твой_ник",
            parse_mode="Markdown"
        )
        return

    # --- ШАГ 3: РЕЖИМ ОБЩЕНИЯ ---
    if current_state == "chat":
        if m.text and not m.text.startswith('/'):
            await m.reply(f"💬 Ты сказал: {m.text}\n\n(Пока это заглушка. Скоро здесь будет GPT!)")
            return
        if m.voice:
            await m.reply(
                "🎧 Голосовые сообщения пока в разработке.\n"
                "Скоро я научусь их распознавать и отвечать голосом! 🚀"
            )
            return

    # --- ШАГ 4: Если пользователь пишет текст без кнопки и не в разделе ---
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

    # --- ШАГ 5: Голосовые (если не в чате) ---
    if m.voice:
        await m.reply(
            "🎧 Голосовые сообщения пока в разработке.\n"
            "Скоро я научусь их распознавать и отвечать голосом! 🚀",
            reply_markup=main_menu()
        )
        return