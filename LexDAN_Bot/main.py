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
from handlers import start, common, voice, chat, lessons, lessons_grammar, lessons_vocabulary, lessons_listening, lessons_reading, lessons_street, lessons_sections, profile, collection, menu, payments, secret_missions, daily_fire, exclusive_rico, admin, courses, daily_reviews, a0_course, onboard_guided, onboard_funnel, path_course, notify

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
    onboard_guided.router,  # /imit_start · слайды to be до catch-all
    onboard_funnel.router,  # inline CTA Общаться / Listening после онбординга
    admin.router,  # админ-команды до catch-all
    exclusive_rico.router,  # /test_winners + эксклюзив паки
    common.router,
    daily_fire.router,  # Огонь дня до catch-all меню
    secret_missions.router,  # кнопка секрета до catch-all меню
    path_course.router,  # новый ежедневный курс (кнопка Курсы)
    courses.router,  # старый placement — не открываем
    a0_course.router,  # пилот A0.T1 L1 (/a0_curs) до voice/меню
    menu.router,
    payments.router,
    voice.router,
    lessons_vocabulary.router,
    lessons_street.router,  # Живая речь до grammar voice catch-all
    lessons_grammar.router,
    lessons_listening.router,  # Listening до заглушек секций
    lessons_reading.router,  # Reading (тест MANAGER) до заглушек
    lessons_sections.router,
    chat.router,
    lessons.router,
    daily_reviews.router,  # после lessons: иначе hub=grammar_review перехватывает уровни
    notify.router,
    collection.router,  # до profile catch-all
    profile.router,
)

app = Flask(__name__)
_loop: asyncio.AbstractEventLoop | None = None

# Голоса, разрешённые для веб-теста уровня (CHAT_VOICES без Rico)
_WEB_TTS_VOICE_IDS = frozenset(
    {
        "NfUrCNRReUL9RXS9upG1",  # Scotty
        "nDJIICjR9zfJExIFeSCN",  # Emmaline
        "av1BMOR1GPgThz9p4fLo",  # Joe
        "dHd5gvgSOzSfduK4CvEg",  # Ed
        "wSqOdjeNqDrHcoK0zorF",  # Lucas
        "TC0Zp7WVFzhA8zpTlRqV",  # Aria
        "YLbQE9U7P1K6rBNJWNSv",  # Jimbo
        "b8gbDO0ybjX1VA89pBdX",  # Ruby
    }
)


def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/")
def home():
    return "LexDAN is running!"


@app.route("/api/tts", methods=["POST", "OPTIONS"])
def api_tts():
    """Озвучка для веб-теста уровня (ElevenLabs, как в боте)."""
    if request.method == "OPTIONS":
        return _cors(app.make_response(("", 204)))

    data = request.get_json(silent=True) or {}
    text = str(data.get("text") or "").strip()
    voice_id = str(data.get("voice_id") or "").strip()

    if not text:
        return _cors(jsonify({"error": "empty text"})), 400
    if len(text) > 500:
        return _cors(jsonify({"error": "text too long"})), 400
    if voice_id not in _WEB_TTS_VOICE_IDS:
        return _cors(jsonify({"error": "invalid voice"})), 400

    try:
        from flask import Response
        from services.elevenlabs import elevenlabs_tts

        audio = elevenlabs_tts(text, voice_id=voice_id, timeout=12)
    except Exception as e:
        logging.error(f"/api/tts error: {e}")
        return _cors(jsonify({"error": "tts failed"})), 502

    if not audio:
        return _cors(jsonify({"error": "tts unavailable"})), 502

    resp = Response(audio, mimetype="audio/mpeg")
    return _cors(resp)


@app.route("/web/", defaults={"filename": "index.html"})
@app.route("/web/<path:filename>")
def website_static(filename):
    """Раздача лендинга с того же хоста (тест уровня → /api/tts без CORS-мучений)."""
    from flask import send_from_directory

    root = os.path.join(os.path.dirname(__file__), "website")
    return send_from_directory(root, filename)


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
        try:
            from services.promo import PROMO_BUILD_ID, PROMO_CODES

            n_life = sum(
                1
                for m in PROMO_CODES.values()
                if m.get("kind") == "lifetime_full_price" and m.get("active") is not False
            )
            logging.info("Promo build %s · lifetime codes=%s", PROMO_BUILD_ID, n_life)
        except Exception as e:
            logging.warning("Promo module load check failed: %s", e)
        if PUBLIC_BASE_URL:
            logging.info(f"YooKassa webhook URL: {PUBLIC_BASE_URL}/yookassa/webhook")
        else:
            logging.info("PUBLIC_BASE_URL пуст — укажи его в env для уведомлений ЮKassa")
        asyncio.create_task(_notify_loop())
        asyncio.create_task(_autorenew_loop())
        asyncio.create_task(_event_finalize_loop())
        asyncio.create_task(_event_announce_once())
        asyncio.create_task(_batch_3d_grant_once())
        asyncio.create_task(_street_talk_channel_post_once())
        asyncio.create_task(_street_talk_dm_broadcast_once())
        await dp.start_polling(bot, handle_as_tasks=True)
    finally:
        release_bot_lock()



async def _batch_3d_grant_once():
    """Разовый грант 3 дней безлимита списку + DM."""
    from services.reg_campaign import deliver_batch_3d_trials

    await asyncio.sleep(25)
    try:
        result = await deliver_batch_3d_trials(bot)
        logging.info("Batch 3d trial grant: %s", result)
    except Exception as e:
        logging.error(f"Batch 3d grant error: {e}")


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




async def _street_talk_channel_post_once():
    """После деплоя один раз пост в канал про Живую речь."""
    from services.broadcast import post_street_talk_to_channel_once

    await asyncio.sleep(40)
    try:
        result = await post_street_talk_to_channel_once(bot, force=False)
        if result.get("already"):
            logging.info("Street talk channel post already sent")
        elif result.get("ok"):
            logging.info("Street talk channel post ok: %s", result)
        else:
            logging.warning("Street talk channel post: %s", result)
    except Exception as e:
        logging.error(f"Street talk channel post error: {e}")


async def _street_talk_dm_broadcast_once():
    """После деплоя один раз разослать всем: Живая речь открыта."""
    from services.broadcast import broadcast_street_talk_once

    await asyncio.sleep(45)
    try:
        result = await broadcast_street_talk_once(bot, force=False)
        if result.get("already"):
            logging.info("Street talk DM broadcast already sent")
        elif result.get("ok"):
            logging.info(
                "Street talk DM sent=%s fail=%s",
                result.get("sent"),
                result.get("fail"),
            )
        else:
            logging.warning("Street talk DM broadcast: %s", result)
    except Exception as e:
        logging.error(f"Street talk DM broadcast error: {e}")


async def _notify_loop():
    """Новая система уведомлений: раз в 5 мин (1 push/день/юзер, приоритет)."""
    from services.notify_engine import send_due_notifications

    await asyncio.sleep(55)
    while True:
        try:
            result = await send_due_notifications(bot)
            if result.get("sent"):
                logging.info("Notify tick: %s", result)
            week = result.get("week") or {}
            if week.get("ok"):
                logging.info("Week results: %s", week)
        except Exception as e:
            logging.error(f"Notify loop error: {e}")
        await asyncio.sleep(300)


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
