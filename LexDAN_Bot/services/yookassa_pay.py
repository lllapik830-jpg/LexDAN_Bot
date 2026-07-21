"""
ЮKassa: создание платежей, webhook, автопродление подписки.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

import requests

from config import (
    BOT_USERNAME,
    PUBLIC_BASE_URL,
    YOOKASSA_SECRET_KEY,
    YOOKASSA_SHOP_ID,
)
from services.database import get_user, load_users, save_users
from services.growth import ensure_growth, extend_premium
from services.pricing import chat_price, consume_discount, full_price
from services.rewards import extend_chat_pass

log = logging.getLogger(__name__)

API = "https://api.yookassa.ru/v3"
SUB_DAYS = 30
PLAN_CHAT = "chat"
PLAN_FULL = "full"


class YooKassaError(RuntimeError):
    def __init__(self, message: str, *, status: int = 0, code: str = ""):
        super().__init__(message)
        self.status = status
        self.code = code


def yookassa_configured() -> bool:
    return bool(YOOKASSA_SHOP_ID and YOOKASSA_SECRET_KEY)


def webhook_url() -> str:
    if not PUBLIC_BASE_URL:
        return ""
    return f"{PUBLIC_BASE_URL}/yookassa/webhook"


def _auth() -> tuple[str, str]:
    return YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY


def _return_url() -> str:
    uname = (BOT_USERNAME or "").lstrip("@")
    if uname:
        return f"https://t.me/{uname}"
    if PUBLIC_BASE_URL:
        return PUBLIC_BASE_URL
    return "https://t.me/"


def _rub(amount: int) -> str:
    return f"{int(amount):.2f}"


def _parse_error(resp: requests.Response) -> YooKassaError:
    code = ""
    desc = resp.text[:300]
    try:
        data = resp.json()
        code = str(data.get("code") or "")
        desc = str(data.get("description") or data.get("parameter") or desc)
    except Exception:
        pass
    return YooKassaError(desc, status=resp.status_code, code=code)


def create_payment(
    *,
    user_id: str,
    plan: str,
    amount_rub: int,
    description: str,
    save_method: bool = True,
) -> dict[str, Any]:
    """
    Создать платёж с редиректом на страницу ЮKassa.
    Если сохранение карты недоступно магазину — повторяем без save_payment_method.
    """
    if not yookassa_configured():
        raise YooKassaError("ЮKassa не настроена: нет YOOKASSA_SHOP_ID / YOOKASSA_SECRET_KEY")

    def _post(with_save: bool) -> dict[str, Any]:
        payload = {
            "amount": {"value": _rub(amount_rub), "currency": "RUB"},
            "capture": True,
            "confirmation": {
                "type": "redirect",
                "return_url": _return_url(),
            },
            "description": description[:128],
            "metadata": {
                "user_id": str(user_id),
                "plan": plan,
                "kind": "initial",
            },
        }
        if with_save:
            payload["save_payment_method"] = True
        r = requests.post(
            f"{API}/payments",
            auth=_auth(),
            headers={
                "Idempotence-Key": str(uuid.uuid4()),
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        if r.status_code >= 400:
            err = _parse_error(r)
            log.error("YooKassa create_payment %s: %s", r.status_code, r.text[:500])
            raise err
        return r.json()

    try:
        return _post(bool(save_method))
    except YooKassaError as e:
        low = str(e).lower()
        # автоплатежи ещё не открыли магазину — даём обычную разовую оплату
        if save_method and (
            "save payment method" in low
            or "forbidden" in low
            or e.code in {"forbidden", "invalid_request"}
        ):
            log.warning("Retry payment without save_payment_method: %s", e)
            return _post(False)
        raise


def create_recurring_payment(
    *,
    user_id: str,
    plan: str,
    amount_rub: int,
    payment_method_id: str,
    description: str,
) -> dict[str, Any]:
    if not yookassa_configured():
        raise RuntimeError("ЮKassa не настроена")

    payload = {
        "amount": {"value": _rub(amount_rub), "currency": "RUB"},
        "capture": True,
        "payment_method_id": payment_method_id,
        "description": description[:128],
        "metadata": {
            "user_id": str(user_id),
            "plan": plan,
            "kind": "renew",
        },
    }
    r = requests.post(
        f"{API}/payments",
        auth=_auth(),
        headers={
            "Idempotence-Key": str(uuid.uuid4()),
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    if r.status_code >= 400:
        log.error("YooKassa renew %s: %s", r.status_code, r.text[:500])
        r.raise_for_status()
    return r.json()


def fetch_payment(payment_id: str) -> dict[str, Any]:
    r = requests.get(
        f"{API}/payments/{payment_id}",
        auth=_auth(),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def confirmation_url(payment: dict) -> str:
    conf = payment.get("confirmation") or {}
    return (conf.get("confirmation_url") or "").strip()


def _already_processed(user: dict, payment_id: str) -> bool:
    done = user.get("yookassa_processed_ids") or []
    return payment_id in done


def _mark_processed(user: dict, payment_id: str) -> None:
    done = list(user.get("yookassa_processed_ids") or [])
    if payment_id not in done:
        done.append(payment_id)
    user["yookassa_processed_ids"] = done[-40:]


def apply_successful_payment(payment: dict) -> dict[str, Any] | None:
    """
    Выдать подписку по успешному платежу.
    Возвращает {user_id, plan, days, renew} или None если уже обработан / битые данные.
    """
    if (payment.get("status") or "") != "succeeded":
        return None

    payment_id = str(payment.get("id") or "")
    meta = payment.get("metadata") or {}
    user_id = str(meta.get("user_id") or "").strip()
    plan = str(meta.get("plan") or "").strip()
    if not payment_id or not user_id or plan not in (PLAN_CHAT, PLAN_FULL):
        log.warning("YooKassa payment missing meta: %s", payment_id)
        return None

    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)

    if _already_processed(user, payment_id):
        return None

    if plan == PLAN_CHAT:
        extend_chat_pass(user, SUB_DAYS)
    else:
        extend_premium(user, SUB_DAYS)

    consume_discount(user)
    _mark_processed(user, payment_id)

    pm = payment.get("payment_method") or {}
    if pm.get("saved") and pm.get("id"):
        user["yookassa_payment_method_id"] = str(pm["id"])
        user["sub_auto"] = True
    elif meta.get("kind") == "renew" and user.get("yookassa_payment_method_id"):
        user["sub_auto"] = True

    user["sub_plan"] = plan
    user["sub_renew_at"] = time.time() + SUB_DAYS * 86400
    user["yookassa_last_payment_id"] = payment_id
    user.pop("yookassa_renew_pending_id", None)

    save_users(users, only=user_id)
    return {
        "user_id": user_id,
        "plan": plan,
        "days": SUB_DAYS,
        "renew": meta.get("kind") == "renew",
        "auto": bool(user.get("sub_auto")),
    }


def handle_webhook_payload(body: dict) -> dict[str, Any] | None:
    """
    Обработать тело HTTP-уведомления ЮKassa.
    Для payment.succeeded дополнительно сверяем платёж через API.
    """
    event = (body.get("event") or "").strip()
    obj = body.get("object") or {}

    if event == "payment.succeeded":
        payment_id = str(obj.get("id") or "")
        if not payment_id or not yookassa_configured():
            return None
        try:
            payment = fetch_payment(payment_id)
        except Exception as e:
            log.error("YooKassa fetch failed: %s", e)
            payment = obj
        return apply_successful_payment(payment)

    if event == "payment_method.active":
        # привязка карты без платежа (если когда-нибудь понадобится)
        return None

    if event == "payment.canceled":
        meta = obj.get("metadata") or {}
        user_id = str(meta.get("user_id") or "").strip()
        if user_id and meta.get("kind") == "renew":
            users = load_users()
            user = get_user(users, user_id)
            user["sub_auto"] = False
            user.pop("yookassa_renew_pending_id", None)
            save_users(users, only=user_id)
            return {"user_id": user_id, "canceled_renew": True}
        return None

    return None


def plan_amount_for_user(user: dict, plan: str) -> int:
    if plan == PLAN_CHAT:
        price, _ = chat_price(user)
        return int(price)
    price, _ = full_price(user)
    return int(price)


def plan_title(plan: str) -> str:
    if plan == PLAN_CHAT:
        return "Общение"
    return "Безлимит ко всему"


def disable_autorenew(user_id: str) -> bool:
    users = load_users()
    user = get_user(users, user_id)
    if not user.get("sub_auto") and not user.get("yookassa_payment_method_id"):
        return False
    user["sub_auto"] = False
    save_users(users, only=user_id)
    return True


def process_due_autorenewals(*, limit: int = 40) -> list[dict]:
    """Списать оплату у тех, у кого подошёл срок автопродления."""
    if not yookassa_configured():
        return []

    now = time.time()
    users = load_users()
    results: list[dict] = []
    n = 0

    for uid, user in list(users.items()):
        if n >= limit:
            break
        if not isinstance(user, dict):
            continue
        if not user.get("sub_auto"):
            continue
        pm_id = (user.get("yookassa_payment_method_id") or "").strip()
        if not pm_id:
            continue
        renew_at = float(user.get("sub_renew_at") or 0)
        if renew_at <= 0:
            continue
        # списываем, когда срок наступил (или остался ≤1 часа)
        if renew_at > now + 3600:
            continue
        if user.get("yookassa_renew_pending_id"):
            continue

        plan = (user.get("sub_plan") or PLAN_FULL).strip()
        if plan not in (PLAN_CHAT, PLAN_FULL):
            plan = PLAN_FULL

        try:
            amount = plan_amount_for_user(user, plan)
            payment = create_recurring_payment(
                user_id=str(uid),
                plan=plan,
                amount_rub=amount,
                payment_method_id=pm_id,
                description=f"LexDAN автопродление: {plan_title(plan)}",
            )
            user["yookassa_renew_pending_id"] = payment.get("id")
            # если сразу succeeded (редко) — применим тут же
            if payment.get("status") == "succeeded":
                save_users(users, only=str(uid))
                applied = apply_successful_payment(payment)
                if applied:
                    results.append(applied)
            else:
                save_users(users, only=str(uid))
                results.append({"user_id": str(uid), "pending": payment.get("id")})
            n += 1
        except Exception as e:
            log.error("Autorenew failed for %s: %s", uid, e)
            user["sub_auto"] = False
            user.pop("yookassa_renew_pending_id", None)
            save_users(users, only=str(uid))
            results.append({"user_id": str(uid), "error": str(e)})
            n += 1

    return results
