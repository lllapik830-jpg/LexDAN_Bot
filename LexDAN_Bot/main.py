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
from handlers import start, common, voice, chat, lessons, lessons_grammar, lessons_vocabulary, lessons_sections, profile, menu, payments, secret_missions, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    start.router,
    admin.router,  # админ-команды до catch-all
    common.router,
    secret_missions.router,  # кнопка секрета до catch-all меню
    menu.router,
    payments.router,
    voice.router,
    lessons_vocabulary.router,
    lessons_grammar.router,
    lessons_sections.router,
    chat.router,
    lessons.router,
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
    asyncio.create_task(_autorenew_loop())
    await dp.start_polling(bot)


async def _reminder_loop():
    """Раз в час проверяем, кому напомнить про занятие."""
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
