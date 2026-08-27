import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data.path_course import (
    LESSONS,
    LESSON_COUNT,
    RANK_CHANGE,
    SKIP_1,
    SKIP_2,
    SKIP_3,
    WELCOME_HTML,
    get_lesson,
    rank_for_score,
    skip_html,
)
from services.path_course import (
    check_answer,
    done_today,
    ensure_path,
    handle_answer,
    handle_next,
    note_open,
    present,
    start_or_resume,
)

assert LESSON_COUNT == 40 and len(LESSONS) == 40
assert get_lesson(1)["steps"]
assert get_lesson(2)["steps"] is None
assert get_lesson(10)["exam"] and get_lesson(10)["target"] == 1.5
assert get_lesson(20)["target"] == 2.0
assert get_lesson(30)["target"] == 2.2
assert get_lesson(40)["target"] == 2.5
assert rank_for_score(1.0)[1].startswith("🌱")
assert rank_for_score(1.5)[1].startswith("📖")
assert "вчера" in skip_html(1)
assert "второй" in skip_html(2)
assert "несколько" in skip_html(3)
for blob in (SKIP_1, SKIP_2, SKIP_3, WELCOME_HTML, RANK_CHANGE):
    assert "заплатил" not in blob.lower()
assert "{rank}" in RANK_CHANGE
assert check_answer("name", "My name is Anna")
assert check_answer("name", "I'm Dan")
assert check_answer("bee", "би")
assert check_answer("cab", "cab")
assert check_answer("goodbye", "Goodbye!")
assert not check_answer("cab", "cat")

u = {"path": {}}
p = ensure_path(u)
assert p["score"] == 1.0 and p["lesson"] == 1

from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))
today = datetime.now(MSK).date()
p["last_done"] = (today - timedelta(days=3)).isoformat()
p["skip_checked_on"] = ""
n = note_open(u)
assert n >= 1

u2 = {"path": {}}
ensure_path(u2)
payload = start_or_resume(u2)
assert payload.get("kb") == "next"
payload = handle_next(u2)
assert payload.get("kb") == "mcq"
payload = handle_answer(u2, "Hi")
assert payload.get("kb") == "next"
payload = handle_next(u2)
assert payload.get("kb") == "text"
payload = handle_answer(u2, "My name is Anna")
assert payload.get("kb") == "text"
payload = handle_answer(u2, "би")
payload = handle_answer(u2, "cab")
assert payload.get("kb") == "text"
payload = handle_answer(u2, "My name is Anna")
payload = handle_answer(u2, "Goodbye")
assert payload.get("kb") == "mcq"
for ans in ("Good morning", "Good evening", "Goodbye", "Nice to meet you too"):
    payload = handle_answer(u2, ans)
assert payload.get("finished") is True
assert u2["path"]["lesson"] == 1
assert u2["path"]["last_done"]
assert done_today(u2)
blocked = start_or_resume(u2)
assert blocked.get("blocked") is True
assert u2["path"]["lesson"] == 1

u3 = {"path": {"lesson": 2, "score": 1.0, "rank": "🌱 Новичок"}}
ensure_path(u3)
stub = present(u3)
assert stub.get("stub") is True
assert u3["path"]["lesson"] == 2
print("ok")
