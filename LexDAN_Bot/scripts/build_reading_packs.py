# -*- coding: utf-8 -*-
"""Собрать reading_packs.py из curated источников _rp_*.py"""
from __future__ import annotations

import pprint
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data._rp_a0a1 import PACKS as P1  # noqa: E402
from data._rp_a2b1 import PACKS as P2  # noqa: E402
from data._rp_b2c1 import PACKS as P3  # noqa: E402
from data._rp_c2 import PACKS as P4  # noqa: E402
from data.reading_topics import READING_TOPICS  # noqa: E402
from services.reading_gen import _pack_structurally_ok  # noqa: E402


def _freeze(pack: dict) -> dict:
    answers = list(pack["answers"])
    bank = list(pack["word_bank"])
    need = {a.lower() for a in answers}
    extra = next((w for w in bank if w.lower() not in need), "purple")
    return {
        "full_text": pack["full_text"],
        "gapped_text": pack["gapped_text"],
        "answers": answers,
        "word_bank": answers + [extra],
        "questions": pack["questions"],
        "plan": pack["plan"],
        "facts": pack["facts"],
    }


def main() -> None:
    raw: dict[str, dict[str, dict]] = {}
    for src in (P1, P2, P3, P4):
        for lv, m in src.items():
            raw.setdefault(lv, {}).update(m)

    packs: dict[str, dict[str, dict]] = {}
    bad = []
    missing = []
    for level, topics in READING_TOPICS.items():
        packs[level] = {}
        for t in topics:
            tid = t["id"]
            if tid not in raw.get(level, {}):
                missing.append((level, tid))
                continue
            p = _freeze(raw[level][tid])
            reason = _pack_structurally_ok(p)
            if reason:
                bad.append((level, tid, reason))
            packs[level][tid] = p

    out = ROOT / "data" / "reading_packs.py"
    header = '''"""Фиксированные Reading-пакеты: все уровни и темы.

Собрано из curated источников data/_rp_*.py через scripts/build_reading_packs.py.
В рантайме GPT для текстов не вызывается.
"""

from __future__ import annotations

READING_PACKS: dict[str, dict[str, dict]] = '''
    body = pprint.pformat(packs, width=100, sort_dicts=False)
    footer = '''


def get_reading_pack(level: str, topic_id: str) -> dict | None:
    lvl = (level or "A1").upper()
    tid = (topic_id or "").strip()
    block = READING_PACKS.get(lvl) or {}
    pack = block.get(tid)
    if not pack:
        return None
    return {
        "full_text": pack["full_text"],
        "gapped_text": pack["gapped_text"],
        "answers": list(pack["answers"]),
        "word_bank": list(pack["word_bank"]),
        "questions": [dict(q) for q in pack["questions"]],
        "plan": list(pack["plan"]),
        "facts": list(pack["facts"]),
    }
'''
    out.write_text(header + body + footer, encoding="utf-8")
    print(f"wrote {out} topics={sum(len(v) for v in packs.values())} bad={bad} missing={missing}")


if __name__ == "__main__":
    main()
