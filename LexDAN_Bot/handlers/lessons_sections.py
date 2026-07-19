"""Заготовки разделов Listening / Reading / Speaking / Writing."""

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.filters import ModeFilter
from handlers.lesson_keyboards import level_sections_kb
from services.database import MODE_LESSONS, load_users, get_user
from services.lesson_state import assessment_busy, ensure_lesson, set_level_hub, set_section_stub

router = Router()

SECTION_BUTTONS = {
    "🎧 Listening": "listening",
    "📖 Reading": "reading",
    "🗣 Speaking": "speaking",
    "✍️ Writing": "writing",
}


def _stub_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True,
    )


@router.message(ModeFilter(MODE_LESSONS), F.text.in_(set(SECTION_BUTTONS)))
async def section_stub_open(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if (user.get("lesson") or {}).get("hub") != "level_hub":
        return
    set_section_stub(str(m.from_user.id), SECTION_BUTTONS[m.text])
    from services.rewards import has_sections_unlock
    from services.growth import ensure_growth

    ensure_growth(user)
    if has_sections_unlock(user):
        await m.answer(
            f"{m.text}\n\n"
            "🔓 У тебя открыт эксклюзивный доступ к разделам (награда за серию)!\n"
            "Контент раздела ещё собираем — совсем скоро здесь появятся задания. "
            "Место за тобой забронировано 🦜",
            reply_markup=_stub_kb(),
        )
    else:
        await m.answer(
            f"{m.text}\n\nЭтот раздел скоро появится! 🚀\n"
            "На тарифе 799 за серию 14 дней можно получить ранний доступ.",
            reply_markup=_stub_kb(),
        )


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ Назад")
async def section_stub_back(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    hub = (user.get("lesson") or {}).get("hub") or ""
    if not str(hub).startswith("stub_"):
        return
    level = user["lesson"].get("level") or user.get("level") or "A1"
    set_level_hub(str(m.from_user.id), level)
    await m.answer(
        f"🎓 Уровень {level} — выбери раздел:",
        reply_markup=level_sections_kb(),
    )
