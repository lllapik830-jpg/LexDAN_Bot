"""
Точка входа бота.
"""

import asyncio
import logging
import os
import threading

from aiogram import Bot, Dispatcher
from flask import Flask, jsonify, request

from config import BOT_TOKEN, PUBLIC_BASE_URL
from handlers import start, common, voice, chat, lessons, lessons_grammar, lessons_vocabulary, lessons_listening, lessons_reading, lessons_sections, profile, collection, menu, payments, secret_missions, daily_fire, exclusive_rico, admin, courses

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

from services.timing_middleware import TimingMiddleware
from services.rate_limit_middleware import RateLimitMiddleware

dp.update.middleware(RateLimitMiddleware())
dp.update.middleware(TimingMiddleware())

dp.include_routers(
    start.router,
    admin.router,  # админ-команды до catch-all
    exclusive_rico.router,  # /test_winners + эксклюзив паки
    common.router,
    daily_fire.router,  # Огонь дня до catch-all меню
    secret_missions.router,  # кнопка секрета до catch-all меню
    courses.router,  # курсы / placement до catch-all меню
    menu.router,
    payments.router,
    voice.router,
    lessons_vocabulary.router,
    lessons_grammar.router,
    lessons_listening.router,  # Listening до заглушек секций
    lessons_reading.router,  # Reading (тест MANAGER) до заглушек
    lessons_sections.router,
    chat.router,
    lessons.router,
    collection.router,  # до profile catch-all
    profile.router,
)

app = Flask(__name__)
_loop: asyncio.AbstractEventLoop | None = None


@app.route("/")
def home():
    return "LexDAN is running!"


@app.route("/yookassa/webhook", methods=["POST"])
def yookassa_webhook():
    """HTTP-уведомления ЮKassa → выдача подписки."""
    try:
        body = request.get_json(force=True, silent=True) or {}
    except Exception:
        body = {}

    try:
        from services.yookassa_pay import handle_webhook_payload, plan_title

        result = handle_webhook_payload(body)
    except Exception as e:
        logging.error(f"YooKassa webhook error: {e}")
        return jsonify({"ok": False}), 200

    if result and result.get("user_id") and _loop is not None:
        uid = int(result["user_id"])
        if result.get("canceled_renew"):
            text = (
                "⚠️ Не удалось продлить подписку автоматически.\n"
                "Автопродление выключено — оформи тариф заново в профиле."
            )
        else:
            title = plan_title(result.get("plan") or "full")
            auto = " Автопродление включено." if result.get("auto") else ""
            verb = "продлена" if result.get("renew") else "активирована"
            if result.get("plan") == "upgrade":
                text = (
                    f"✅ <b>Апгрейд</b> до полного доступа {verb} на "
                    f"{result.get('days', 30)} дн.{auto}\n"
                    "Теперь безлимит уроков, все голоса и 150 тем 🚀"
                )
            else:
                text = (
                    f"✅ Подписка <b>{title}</b> {verb} на "
                    f"{result.get('days', 30)} дн.{auto}"
                )
        asyncio.run_coroutine_threadsafe(
            bot.send_message(uid, text, parse_mode="HTML"),
            _loop,
        )

    return jsonify({"ok": True}), 200


def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


async def main():
    global _loop
    _loop = asyncio.get_running_loop()

    from services.bot_lock import release_bot_lock, wait_for_bot_lock

    # Только один процесс имеет право на getUpdates
    got = await wait_for_bot_lock(max_wait_sec=90)
    if not got:
        logging.error(
            "Another LexDAN instance already polls Telegram. "
            "Exit to avoid TelegramConflictError."
        )
        return

    try:
        # Сбрасываем старые апдейты и webhook — меньше двойных ответов
        await bot.delete_webhook(drop_pending_updates=True)
        db = "Postgres" if os.getenv("DATABASE_URL") else "users.json (file)"
        print(f"🤖 LexDAN is running! Storage: {db}")
        logging.info(f"User storage backend: {db}")
        if PUBLIC_BASE_URL:
            logging.info(f"YooKassa webhook URL: {PUBLIC_BASE_URL}/yookassa/webhook")
        else:
            logging.info("PUBLIC_BASE_URL пуст — укажи его в env для уведомлений ЮKassa")
        asyncio.create_task(_reminder_loop())
        asyncio.create_task(_trial_last_day_offer_loop())
        asyncio.create_task(_autorenew_loop())
        asyncio.create_task(_event_finalize_loop())
        asyncio.create_task(_event_announce_once())
        await dp.start_polling(bot, handle_as_tasks=True)
    finally:
        release_bot_lock()


async def _event_announce_once():
    """После старта сервиса — разослать анонс ивента один раз (если ещё не слали)."""
    from services.event_magic import broadcast_event_start, is_event_active

    await asyncio.sleep(20)
    try:
        if not is_event_active():
            return
        result = await broadcast_event_start(bot, force=False)
        if result.get("already"):
            logging.info("Event announce already sent earlier")
        elif result.get("ok"):
            logging.info(
                "Event announce sent=%s fail=%s",
                result.get("sent"),
                result.get("fail"),
            )
    except Exception as e:
        logging.error(f"Event announce error: {e}")


async def _reminder_loop():
    """Раз в час: напоминания «не заходил»."""
    from services.reminders import send_due_reminders

    await asyncio.sleep(45)  # дать боту подняться
    while True:
        try:
            n = await send_due_reminders(bot)
            if n:
                logging.info(f"Reminders sent: {n}")
        except Exception as e:
            logging.error(f"Reminder loop error: {e}")
        await asyncio.sleep(3600)


async def _trial_last_day_offer_loop():
    """Раз в 6 часов: оффер последнего дня триала (−15%)."""
    from services.trial_last_day import send_due_last_day_offers

    await asyncio.sleep(90)
    while True:
        try:
            offer = await send_due_last_day_offers(bot)
            if offer.get("sent"):
                logging.info("Trial last-day offers: %s", offer)
        except Exception as e:
            logging.error(f"Trial last-day offer loop error: {e}")
        await asyncio.sleep(6 * 3600)


async def _event_finalize_loop():
    """Раз в 15 мин — авто-итоги ивента после EVENT_END + рассылка призов."""
    from services.event_magic import maybe_auto_finalize, load_event_state
    from services.event_prize_delivery import deliver_all_prizes

    await asyncio.sleep(60)
    while True:
        try:
            result = await asyncio.to_thread(maybe_auto_finalize)
            if result and not result.get("already"):
                logging.info(
                    "Magic event auto-finalized, top=%s",
                    len(result.get("top") or []),
                )
                delivery = await deliver_all_prizes(bot, result.get("top") or [])
                logging.info("Prize delivery: %s", delivery)
            else:
                # если финал уже был, а рассылка ещё нет — дослать
                st = await asyncio.to_thread(load_event_state)
                if st.get("finalized") and not st.get("prizes_delivered"):
                    delivery = await deliver_all_prizes(bot)
                    logging.info("Prize delivery (catch-up): %s", delivery)
        except Exception as e:
            logging.error(f"Event finalize loop error: {e}")
        await asyncio.sleep(900)


async def _autorenew_loop():
    """Раз в час — автосписания ЮKassa по сохранённым картам."""
    from services.yookassa_pay import process_due_autorenewals, yookassa_configured

    await asyncio.sleep(90)
    while True:
        try:
            if yookassa_configured():
                results = await asyncio.to_thread(process_due_autorenewals)
                if results:
                    logging.info(f"Autorenew batch: {len(results)}")
                    for r in results:
                        if r.get("error") and r.get("user_id"):
                            try:
                                await bot.send_message(
                                    int(r["user_id"]),
                                    "⚠️ Автопродление не прошло. "
                                    "Оформи тариф снова в профиле → Подписка.",
                                )
                            except Exception:
                                pass
                        elif r.get("user_id") and r.get("plan"):
                            # успешное списание без webhook (редко) — уже применили
                            from services.yookassa_pay import plan_title

                            try:
                                await bot.send_message(
                                    int(r["user_id"]),
                                    f"✅ Подписка <b>{plan_title(r['plan'])}</b> "
                                    f"продлена на {r.get('days', 30)} дн.",
                                    parse_mode="HTML",
                                )
                            except Exception:
                                pass
        except Exception as e:
            logging.error(f"Autorenew loop error: {e}")
        await asyncio.sleep(3600)


if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    asyncio.run(main())
