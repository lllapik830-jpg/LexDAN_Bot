"""Магические элементы — альбом, гонка лидеров, зал славы."""

from __future__ import annotations

import os

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from handlers.filters import ModeFilter
from handlers.keyboards import profile_menu
from services.database import MODE_PROFILE, load_users, get_user, save_users
from services.growth import ensure_growth
from services.collection import (
    BTN_COLLECTION,
    ensure_collection,
    format_album_text,
    album_numbers_kb,
    owned_ids,
    collection_allowed,
)
from services.event_magic import (
    BTN_HALL_OF_FAME,
    BTN_LEADERBOARD,
    format_hall_of_fame_text,
    format_leaderboard_text_for,
    remember_tg_username,
)
from data.collection_catalog import TOTAL_ELEMENTS, element_by_id, asset_path, RARITY_LABEL_RU

router = Router()

HUB_ALBUM = "collection_album"


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_COLLECTION)
async def open_collection(m: Message):
    if not collection_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ensure_collection(user)
    remember_tg_username(user, getattr(m.from_user, "username", None))
    user["collection_hub"] = HUB_ALBUM
    save_users(users, only=str(m.from_user.id))
    await m.answer(
        format_album_text(user),
        reply_markup=album_numbers_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_LEADERBOARD)
async def open_leaderboard(m: Message):
    if not collection_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    remember_tg_username(user, getattr(m.from_user, "username", None))
    user["collection_hub"] = ""
    save_users(users, only=uid)
    await m.answer(
        format_leaderboard_text_for(user, uid, users),
        reply_markup=profile_menu(user, user_id=m.from_user.id),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_HALL_OF_FAME)
async def open_hall_of_fame(m: Message):
    if not collection_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    user["collection_hub"] = ""
    save_users(users, only=uid)
    await m.answer(
        format_hall_of_fame_text(),
        reply_markup=profile_menu(user, user_id=m.from_user.id),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == "⬅️ В профиль")
async def collection_back_profile(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    user["collection_hub"] = ""
    save_users(users, only=str(m.from_user.id))
    await m.answer("📊 Профиль", reply_markup=profile_menu(user, user_id=m.from_user.id))


@router.message(ModeFilter(MODE_PROFILE), F.text.regexp(r"^\d{1,2}$"))
async def collection_show_card(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    if (user.get("collection_hub") or "") != HUB_ALBUM:
        return
    try:
        n = int((m.text or "").strip())
    except ValueError:
        return
    if n < 1 or n > TOTAL_ELEMENTS:
        await m.answer("Выбери номер от 1 до 15.")
        return
    have = owned_ids(user)
    if n not in have:
        await m.answer(
            "🔒 Этот элемент ещё не выпал. Продолжай Grammar, Vocabulary и Listening!"
        )
        return
    el = element_by_id(n)
    if not el:
        return
    rar = RARITY_LABEL_RU.get(el["rarity"], "")
    caption = f"#{n:02d} · {rar}: <b>{el['title_ru']}</b>"
    path = asset_path(n)
    if os.path.isfile(path):
        await m.answer_photo(FSInputFile(path), caption=caption, parse_mode="HTML")
    else:
        await m.answer(caption, parse_mode="HTML")
