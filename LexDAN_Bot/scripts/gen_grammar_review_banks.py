# -*- coding: utf-8 -*-
"""Generate data/grammar_review_banks.py from FALLBACKS.

Review banks: 10 exercises per topic (2 of each subtype), morphologically
swapped so they differ from the main topic bank.

Run: python scripts/gen_grammar_review_banks.py
"""
from __future__ import annotations

import copy
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.grammar_exercise_fallbacks import FALLBACKS  # noqa: E402

OUT = ROOT / "data" / "grammar_review_banks.py"

# EN ↔ EN word swaps (case-preserving via _swap_text)
SWAP_PAIRS: list[tuple[str, str]] = [
    ("cat", "dog"),
    ("cats", "dogs"),
    ("phone", "book"),
    ("phones", "books"),
    ("telephone", "notebook"),
    ("two", "four"),
    ("three", "five"),
    ("five", "seven"),
    ("house", "flat"),
    ("houses", "flats"),
    ("school", "office"),
    ("schools", "offices"),
    ("friend", "brother"),
    ("friends", "brothers"),
    ("table", "desk"),
    ("tables", "desks"),
    ("room", "kitchen"),
    ("rooms", "kitchens"),
    ("bag", "box"),
    ("bags", "boxes"),
    ("book", "pen"),
    ("books", "pens"),
    ("chair", "sofa"),
    ("chairs", "sofas"),
    ("student", "teacher"),
    ("students", "teachers"),
    ("park", "garden"),
    ("window", "door"),
    ("windows", "doors"),
    ("apple", "orange"),
    ("apples", "oranges"),
    ("milk", "water"),
    ("car", "bike"),
    ("cars", "bikes"),
    ("morning", "evening"),
    ("evening", "afternoon"),
    ("city", "town"),
    ("Moscow", "London"),
    ("London", "Paris"),
]

# RU whole-token swaps (whitespace-split; punctuation kept)
RU_SWAP_MAP: dict[str, str] = {
    "кот": "пёс",
    "кота": "пса",
    "кошка": "собака",
    "телефон": "книга",
    "телефона": "книги",
    "книга": "ручка",
    "книги": "ручки",
    "книг": "ручек",
    "две": "четыре",
    "два": "четыре",
    "три": "пять",
    "пять": "семь",
    "дом": "квартира",
    "дома": "квартиры",
    "школа": "офис",
    "школу": "офис",
    "школе": "офисе",
    "друг": "брат",
    "друга": "брата",
    "стол": "парта",
    "стола": "парты",
    "комнате": "кухне",
    "комната": "кухня",
    "сумке": "коробке",
    "сумка": "коробка",
    "яблок": "апельсинов",
    "яблоки": "апельсины",
    "молоко": "вода",
    "молока": "воды",
    "парк": "сад",
    "парка": "сада",
    "окно": "дверь",
    "окна": "двери",
    "студент": "учитель",
    "студентов": "учителей",
    "Москве": "Лондоне",
    "Москву": "Лондон",
}

JUNK_MARKERS = ("wrong1", "wrong2", "wrong3", "option_a", "option_b", "banana", "placeholder")


def _is_junk(item: dict) -> bool:
    blob = " ".join(
        str(v).lower()
        for v in item.values()
        if isinstance(v, (str, list))
    )
    return any(m in blob for m in JUNK_MARKERS)


def _swap_token(tok: str, mapping: dict[str, str]) -> str:
    low = tok.lower()
    # strip trailing punctuation for lookup
    m = re.match(r"^([A-Za-z']+)(.*)$", tok)
    if not m:
        return tok
    core, punct = m.group(1), m.group(2)
    repl = mapping.get(core.lower())
    if not repl:
        return tok
    if core.isupper():
        repl = repl.upper()
    elif core[0].isupper():
        repl = repl[0].upper() + repl[1:]
    return repl + punct


def _build_swap_map(seed: int) -> dict[str, str]:
    """Pick a deterministic direction per pair from seed."""
    rng = random.Random(seed)
    mapping: dict[str, str] = {}
    for a, b in SWAP_PAIRS:
        if rng.random() < 0.5:
            mapping[a.lower()] = b
            mapping[b.lower()] = a
        else:
            mapping[a.lower()] = b
            # avoid cycles colliding: prefer a→b only if not already set
            mapping.setdefault(b.lower(), a)
    return mapping


def _swap_text(text: str, mapping: dict[str, str]) -> str:
    if not text:
        return text
    parts = re.split(r"(\s+)", text)
    out: list[str] = []
    for p in parts:
        if not p or p.isspace():
            out.append(p)
            continue
        out.append(_swap_token(p, mapping))
    return "".join(out)


def _swap_ru(text: str, seed: int) -> str:
    if not text:
        return text
    rng = random.Random(seed)
    parts = re.split(r"(\s+)", text)
    out: list[str] = []
    for p in parts:
        if not p or p.isspace():
            out.append(p)
            continue
        m = re.match(r"^([^\W\d_]+)([^\w]*)$", p, flags=re.UNICODE)
        if not m:
            out.append(p)
            continue
        core, punct = m.group(1), m.group(2)
        repl = RU_SWAP_MAP.get(core)
        if repl and rng.random() < 0.9:
            out.append(repl + punct)
        else:
            out.append(p)
    return "".join(out)


def _deep_swap(obj, mapping: dict[str, str], seed: int):
    if isinstance(obj, str):
        # Cyrillic-heavy → RU swap; else EN swap
        cyr = sum(1 for c in obj if "а" <= c.lower() <= "я" or c in "ёЁ")
        if cyr >= 2:
            return _swap_ru(obj, seed)
        return _swap_text(obj, mapping)
    if isinstance(obj, list):
        return [_deep_swap(x, mapping, seed + i) for i, x in enumerate(obj)]
    if isinstance(obj, dict):
        return {k: _deep_swap(v, mapping, seed + hash(k) % 97) for k, v in obj.items()}
    return obj


def _looks_english_sentence(s: str) -> bool:
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 8:
        return False
    words = s.split()
    if len(words) < 3:
        return False
    cyr = sum(1 for c in s if "а" <= c.lower() <= "я" or c in "ёЁ")
    if cyr > 2:
        return False
    if "____" in s or "(be)" in s or "(not" in s:
        return False
    low = s.lower()
    if low.startswith("which ") or low.startswith("choose "):
        return False
    return True


def _fill_blank(sentence_en: str, answer: str) -> str | None:
    if not sentence_en or "____" not in sentence_en:
        return None
    if not isinstance(answer, str) or not answer.strip():
        return None
    # skip multi-word answers that look like full sentences already
    filled = sentence_en.replace("____", answer.strip(), 1)
    filled = re.sub(r"\s*\([^)]*\)\s*", " ", filled)
    filled = re.sub(r"\s+", " ", filled).strip()
    # drop trailing blank markers
    filled = filled.replace("____", "").strip()
    if not filled.endswith((".", "?", "!")):
        filled += "."
    return filled if _looks_english_sentence(filled) else None


def _collect_en_sentences(items: list[dict], mapping: dict[str, str], seed: int) -> list[tuple[str, str]]:
    """Return list of (en, ru) after swap."""
    seen: set[str] = set()
    out: list[tuple[str, str]] = []

    def add(en: str, ru: str = "") -> None:
        en2 = _swap_text(en, mapping).strip()
        if not en2.endswith((".", "?", "!")):
            en2 = en2 + "."
        key = en2.lower()
        if key in seen or not _looks_english_sentence(en2):
            return
        seen.add(key)
        ru2 = _swap_ru(ru or "", seed + len(out)) if ru else ""
        out.append((en2, ru2))

    for it in items:
        ans = it.get("answer")
        ru = it.get("sentence_ru") or ""
        if _looks_english_sentence(str(ans or "")):
            add(str(ans), ru)
        if it.get("subtype") == "mcq" and _looks_english_sentence(str(ans or "")):
            add(str(ans), ru)
        filled = _fill_blank(it.get("sentence_en") or "", str(ans or ""))
        if filled:
            add(filled, ru)
        # translate_en answers
        if it.get("subtype") == "translate_en" and _looks_english_sentence(str(ans or "")):
            add(str(ans), ru)

    # synthesize from short answers if still short
    if len(out) < 4:
        for it in items:
            ans = str(it.get("answer") or "").strip()
            sen = it.get("sentence_en") or ""
            ru = it.get("sentence_ru") or ""
            if ans and " " not in ans and sen:
                filled = _fill_blank(sen, ans)
                if filled:
                    add(filled, ru)
            if len(out) >= 4:
                break

    if len(out) < 2:
        # last resort templates from topic material
        tip = (items[0].get("tip") or "Practice this form.") if items else "Practice."
        base = items[0] if items else {}
        ans = str(base.get("answer") or "is")
        add(f"There is a dog in the kitchen.", "На кухне есть собака.")
        add(f"She has a book on the desk.", "У неё на парте книга.")
        _ = tip, ans

    return out


def _accept_variants(answer: str) -> list[str]:
    a = answer.strip()
    variants = {a}
    end = a[-1] if a and a[-1] in ".?!" else ""
    core = a[:-1] if end else a

    def with_end(s: str, punct: str = end or ".") -> str:
        s = s.rstrip(".?!")
        return s + punct if punct else s

    variants.add(core)
    variants.add(with_end(core, end or "."))
    # There's / There is
    if core.startswith("There is "):
        variants.add(with_end(core.replace("There is ", "There's ", 1)))
        variants.add(core.replace("There is ", "There's ", 1))
    if core.startswith("There's "):
        variants.add(with_end(core.replace("There's ", "There is ", 1)))
        variants.add(core.replace("There's ", "There is ", 1))
    if core.startswith("There are "):
        variants.add(with_end(core.replace("There are ", "There're ", 1)))
        variants.add(core.replace("There are ", "There're ", 1))
    ordered = [a] + [v for v in sorted(variants) if v != a]
    return ordered[:8]


def _shuffle_words(sentence: str, topic_id: str, i: int) -> list[str]:
    # tokenize keeping punctuation attached or separate trailing .?!
    s = sentence.strip()
    end = ""
    if s and s[-1] in ".?!":
        end = s[-1]
        s = s[:-1].strip()
    words = s.split()
    if end and words:
        # keep period out of tokens (answer has full sentence with punct)
        pass
    rng = random.Random(hash(topic_id) + i)
    shuffled = words[:]
    # ensure not identical to original when possible
    for _ in range(20):
        rng.shuffle(shuffled)
        if shuffled != words or len(words) <= 1:
            break
    return shuffled


def _clean_items(items: list[dict]) -> list[dict]:
    return [it for it in items if isinstance(it, dict) and not _is_junk(it)]


def _ensure_mcq_options(opts: list, answer: str) -> list[str]:
    opts = [str(o) for o in (opts or []) if o is not None]
    # drop junk options
    opts = [o for o in opts if o.lower() not in JUNK_MARKERS and "wrong" not in o.lower()]
    if answer not in opts:
        opts = [answer] + opts
    # pad with distractors
    fillers = ["is", "are", "was", "were", "do", "does", "did", "can", "must", "have"]
    for f in fillers:
        if len(opts) >= 4:
            break
        if f not in opts and f != answer:
            opts.append(f)
    # unique preserve order
    seen = set()
    uniq = []
    for o in opts:
        if o not in seen:
            seen.add(o)
            uniq.append(o)
    opts = uniq
    if len(opts) > 4:
        # keep answer + 3 others
        others = [o for o in opts if o != answer][:3]
        opts = [answer] + others
        # rotate so answer not always first
        opts = opts[1:] + [opts[0]]
    while len(opts) < 4:
        opts.append(f"option{len(opts)}")
    # final: ensure answer in list
    if answer not in opts:
        opts[0] = answer
    return opts[:4]


def _make_mcq(src: dict, mapping: dict[str, str], seed: int) -> dict:
    item = _deep_swap(copy.deepcopy(src), mapping, seed)
    item["kind"] = "mcq"
    item["subtype"] = "mcq"
    ans = str(item.get("answer") or "")
    opts = _ensure_mcq_options(item.get("options") or [], ans)
    # also swap options already done via deep_swap; re-ensure
    item["options"] = opts
    item["answer"] = ans if ans in opts else opts[0]
    item.setdefault("instruction_ru", "Выбери правильный вариант.")
    item.setdefault("sentence_en", "____")
    item.setdefault("sentence_ru", "")
    item.setdefault("tip", "Повтори правило темы.")
    return {
        "kind": "mcq",
        "subtype": "mcq",
        "instruction_ru": item["instruction_ru"],
        "sentence_en": item.get("sentence_en") or "____",
        "sentence_ru": item.get("sentence_ru") or "",
        "options": item["options"],
        "answer": item["answer"],
        "tip": item.get("tip") or "Повтори правило темы.",
    }


def _make_word_form(src: dict, mapping: dict[str, str], seed: int) -> dict:
    item = _deep_swap(copy.deepcopy(src), mapping, seed)
    ans = str(item.get("answer") or "").strip()
    out = {
        "kind": "write",
        "subtype": "word_form",
        "instruction_ru": item.get("instruction_ru") or "Напиши правильную форму.",
        "sentence_en": item.get("sentence_en") or "____",
        "sentence_ru": item.get("sentence_ru") or "",
        "base_form": item.get("base_form") or "",
        "answer": ans,
        "tip": item.get("tip") or "Вставь нужную форму.",
    }
    if item.get("accept"):
        out["accept"] = _deep_swap(item["accept"], mapping, seed + 3)
    return out


def _make_translate_en(src: dict, mapping: dict[str, str], seed: int, en_fallback: str = "") -> dict:
    item = _deep_swap(copy.deepcopy(src), mapping, seed)
    ans = str(item.get("answer") or en_fallback or "").strip()
    if not _looks_english_sentence(ans) and en_fallback:
        ans = _swap_text(en_fallback, mapping)
    ru = item.get("sentence_ru") or ""
    if not ru and en_fallback:
        ru = "Переведи предложение."
    accept = item.get("accept")
    if isinstance(accept, list) and accept:
        accept = [_deep_swap(a, mapping, seed + i) for i, a in enumerate(accept)]
        # ensure swapped answer variants
        for v in _accept_variants(ans):
            if v not in accept:
                accept.append(v)
    else:
        accept = _accept_variants(ans)
    return {
        "kind": "write",
        "subtype": "translate_en",
        "instruction_ru": item.get("instruction_ru") or "Переведи на английский:",
        "sentence_ru": ru,
        "sentence_en": item.get("sentence_en") or "",
        "answer": ans if ans.endswith((".", "?", "!")) else (ans + "." if ans else ans),
        "accept": accept[:10],
        "tip": item.get("tip") or "Переведи внимательно.",
    }


def _make_order_words(en: str, ru: str, topic_id: str, i: int) -> dict:
    words = _shuffle_words(en, topic_id, i)
    ans = en if en.endswith((".", "?", "!")) else en + "."
    return {
        "kind": "write",
        "subtype": "order_words",
        "instruction_ru": "Составь предложение из слов:",
        "sentence_en": "",
        "sentence_ru": ru or "",
        "words": words,
        "answer": ans,
        "accept": _accept_variants(ans),
        "tip": "Subject → Verb → Object (и обстоятельства).",
    }


def _make_write_sentence(en: str, ru: str) -> dict:
    ans = en if en.endswith((".", "?", "!")) else en + "."
    cue = ru or "Составь предложение по смыслу темы."
    return {
        "kind": "write",
        "subtype": "write_sentence",
        "instruction_ru": "Напиши предложение на английском по русской подсказке:",
        "sentence_ru": cue,
        "sentence_en": "",
        "answer": ans,
        "accept": _accept_variants(ans),
        "tip": "Опирайся на структуру из темы; следи за формой глагола.",
    }


def _synth_mcq_from(items: list[dict], mapping: dict[str, str], seed: int) -> dict:
    # Prefer existing mcq; else build from word_form
    for it in items:
        if it.get("subtype") == "mcq":
            return _make_mcq(it, mapping, seed)
    for it in items:
        if it.get("subtype") == "word_form":
            ans = str(it.get("answer") or "is")
            opts = _ensure_mcq_options([ans, "is", "are", "was"], ans)
            src = {
                "instruction_ru": "Выбери правильную форму.",
                "sentence_en": it.get("sentence_en") or f"____ ({it.get('base_form') or 'form'}).",
                "sentence_ru": it.get("sentence_ru") or "",
                "options": opts,
                "answer": ans,
                "tip": it.get("tip") or "Выбери верную форму.",
            }
            return _make_mcq(src, mapping, seed)
    # absolute fallback
    src = {
        "instruction_ru": "Выбери правильный вариант.",
        "sentence_en": "There ____ a dog in the kitchen.",
        "sentence_ru": "На кухне есть собака.",
        "options": ["is", "are", "am", "be"],
        "answer": "is",
        "tip": "Ед. число → is.",
    }
    return _make_mcq(src, mapping, seed)


def _synth_word_form_from(items: list[dict], mapping: dict[str, str], seed: int) -> dict:
    for it in items:
        if it.get("subtype") == "word_form":
            return _make_word_form(it, mapping, seed)
    for it in items:
        if it.get("subtype") == "mcq":
            ans = str(it.get("answer") or "")
            if " " not in ans and ans:
                src = {
                    "instruction_ru": "Напиши правильную форму.",
                    "sentence_en": it.get("sentence_en") or "____",
                    "sentence_ru": it.get("sentence_ru") or "",
                    "base_form": ans,
                    "answer": ans,
                    "tip": it.get("tip") or "Вставь форму.",
                }
                return _make_word_form(src, mapping, seed)
    src = {
        "instruction_ru": "Напиши is или are.",
        "sentence_en": "There ____ a book on the desk.",
        "sentence_ru": "На парте есть книга.",
        "base_form": "be",
        "answer": "is",
        "tip": "a book → is.",
    }
    return _make_word_form(src, mapping, seed)


def build_topic_bank(topic_id: str, raw_items: list[dict]) -> tuple[list[dict], dict]:
    """Return (bank of 10, synth_flags).

    synth_flags keys: mcq, word_form, translate_en, en_sentence
    True = had to pad/reuse/invent because source pool was too small.
    (order_words / write_sentence are always derived — not flagged.)
    """
    items = _clean_items(raw_items)
    flags = {
        "mcq": False,
        "word_form": False,
        "translate_en": False,
        "en_sentence": False,
    }
    seed = abs(hash(topic_id)) % (10**9)
    mapping = _build_swap_map(seed)

    mcq_srcs = [it for it in items if it.get("subtype") == "mcq"]
    wf_srcs = [it for it in items if it.get("subtype") == "word_form"]
    te_srcs = [it for it in items if it.get("subtype") == "translate_en"]

    en_pairs = _collect_en_sentences(items, mapping, seed)
    if len(en_pairs) < 2:
        flags["en_sentence"] = True

    bank: list[dict] = []

    # 2 mcq — prefer later items so less identical to first practice ones
    for i in range(2):
        if len(mcq_srcs) >= 2:
            src = mcq_srcs[-(i + 1)]
            bank.append(_make_mcq(src, mapping, seed + 10 + i))
        elif mcq_srcs:
            flags["mcq"] = True
            bank.append(_make_mcq(mcq_srcs[i % len(mcq_srcs)], mapping, seed + 100 + i * 17))
        else:
            flags["mcq"] = True
            bank.append(_synth_mcq_from(items, mapping, seed + 200 + i))

    # 2 word_form
    for i in range(2):
        if len(wf_srcs) >= 2:
            src = wf_srcs[-(i + 1)]
            bank.append(_make_word_form(src, mapping, seed + 20 + i))
        elif wf_srcs:
            flags["word_form"] = True
            bank.append(_make_word_form(wf_srcs[i % len(wf_srcs)], mapping, seed + 120 + i * 19))
        else:
            flags["word_form"] = True
            bank.append(_synth_word_form_from(items, mapping, seed + 220 + i))

    # 2 order_words
    for i in range(2):
        if i < len(en_pairs):
            en, ru = en_pairs[i]
        elif en_pairs:
            flags["en_sentence"] = True
            en, ru = en_pairs[i % len(en_pairs)]
            en = _swap_text(en, _build_swap_map(seed + 50 + i))
        else:
            flags["en_sentence"] = True
            en, ru = "There is a dog in the kitchen.", "На кухне есть собака."
        bank.append(_make_order_words(en, ru, topic_id, i + 1))

    # 2 translate_en
    for i in range(2):
        if len(te_srcs) >= 2 and i < len(te_srcs):
            en_fb = en_pairs[(i + 2) % len(en_pairs)][0] if en_pairs else ""
            bank.append(_make_translate_en(te_srcs[i], mapping, seed + 30 + i, en_fb))
        elif te_srcs and i == 0:
            en_fb = en_pairs[(i + 2) % len(en_pairs)][0] if en_pairs else ""
            bank.append(_make_translate_en(te_srcs[0], mapping, seed + 30 + i, en_fb))
        elif te_srcs:
            flags["translate_en"] = True
            # second slot: build from an English sentence + RU cue
            if en_pairs:
                en, ru = en_pairs[(i + 2) % len(en_pairs)]
            else:
                en, ru = "I have a book on the desk.", "У меня на парте книга."
            src = {
                "instruction_ru": te_srcs[0].get("instruction_ru") or "Переведи на английский:",
                "sentence_ru": ru or te_srcs[0].get("sentence_ru") or "Переведи предложение.",
                "answer": en,
                "tip": te_srcs[0].get("tip") or "Переведи полностью.",
            }
            bank.append(_make_translate_en(src, mapping, seed + 130 + i * 23, en))
        else:
            flags["translate_en"] = True
            if en_pairs:
                en, ru = en_pairs[(i + 2) % len(en_pairs)]
            else:
                en, ru = "I have a book on the desk.", "У меня на парте книга."
            src = {
                "instruction_ru": "Переведи на английский:",
                "sentence_ru": ru or "Переведи предложение.",
                "answer": en,
                "tip": "Переведи полностью.",
            }
            bank.append(_make_translate_en(src, mapping, seed + 230 + i, en))

    # 2 write_sentence — always derived from EN/RU pairs (not a FALLBACKS subtype)
    for i in range(2):
        idx = (i + 2) % max(len(en_pairs), 1) if en_pairs else 0
        if en_pairs:
            en, ru = en_pairs[idx]
            en = _swap_text(en, _build_swap_map(seed + 70 + i))
            ru = _swap_ru(ru, seed + 80 + i) if ru else ru
        else:
            flags["en_sentence"] = True
            en, ru = "My brother works in the office.", "Мой брат работает в офисе."
        if not ru:
            ru = f"Напиши по-английски: {en}"
            flags["en_sentence"] = True
        bank.append(_make_write_sentence(en, ru))

    assert len(bank) == 10, (topic_id, len(bank))
    counts = Counter(x["subtype"] for x in bank)
    for st in ("mcq", "word_form", "order_words", "translate_en", "write_sentence"):
        assert counts[st] == 2, (topic_id, dict(counts))

    for x in bank:
        if x["subtype"] == "mcq":
            assert x["answer"] in x["options"], (topic_id, x)
            assert len(x["options"]) == 4, (topic_id, x)
        if x["subtype"] == "order_words":
            assert x.get("words") and x.get("answer"), topic_id

    return bank, flags


def generate_all() -> tuple[dict[str, list[dict]], dict[str, dict]]:
    banks: dict[str, list[dict]] = {}
    synth_report: dict[str, dict] = {}
    for topic_id, items in FALLBACKS.items():
        bank, flags = build_topic_bank(topic_id, items)
        banks[topic_id] = bank
        if any(flags.values()):
            synth_report[topic_id] = {k: v for k, v in flags.items() if v}
    return banks, synth_report


def write_output(banks: dict[str, list[dict]]) -> None:
    OUT.write_text(_dump_module(banks), encoding="utf-8")


def _format_value(obj, indent: int = 0) -> str:
    sp = "    " * indent
    sp1 = "    " * (indent + 1)
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = ["{"]
        for k, v in obj.items():
            lines.append(f"{sp1}{k!r}: {_format_value(v, indent + 1)},")
        lines.append(f"{sp}}}")
        return "\n".join(lines)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        # short list of strings on one line if small
        if all(isinstance(x, str) for x in obj) and sum(len(x) for x in obj) < 70:
            return "[" + ", ".join(repr(x) for x in obj) + "]"
        lines = ["["]
        for x in obj:
            lines.append(f"{sp1}{_format_value(x, indent + 1)},")
        lines.append(f"{sp}]")
        return "\n".join(lines)
    return repr(obj)


def _dump_module(banks: dict[str, list[dict]]) -> str:
    parts = [
        '"""Резервные задания для ежедневного повторения Grammar (не из основной темы)."""',
        "",
        "REVIEW_BANKS: dict[str, list[dict]] = {",
    ]
    for tid, items in banks.items():
        parts.append(f"    {tid!r}: [")
        for it in items:
            parts.append(f"        {_format_value(it, 2)},")
        parts.append("    ],")
    parts.append("}")
    parts.append("")
    parts.append("")
    parts.append("def get_review_bank(topic_id: str) -> list[dict]:")
    parts.append("    return list(REVIEW_BANKS.get(topic_id) or [])")
    parts.append("")
    return "\n".join(parts)


def verify(banks: dict[str, list[dict]]) -> None:
    assert len(banks) == 80, len(banks)
    for tid, items in banks.items():
        assert len(items) == 10, (tid, len(items))
        c = Counter(x["subtype"] for x in items)
        for st in ("mcq", "word_form", "order_words", "translate_en", "write_sentence"):
            assert c[st] == 2, (tid, dict(c))


def main() -> None:
    banks, synth_report = generate_all()
    verify(banks)
    write_output(banks)
    # re-import check
    import importlib

    spec_name = "data.grammar_review_banks"
    if spec_name in sys.modules:
        importlib.reload(sys.modules[spec_name])
    else:
        importlib.import_module(spec_name)
    from data.grammar_review_banks import REVIEW_BANKS, get_review_bank

    verify(REVIEW_BANKS)
    print(f"topics: {len(REVIEW_BANKS)}")
    print(f"each bank len: all 10 = {all(len(v) == 10 for v in REVIEW_BANKS.values())}")
    print(f"topics needing synthesis (source shortage): {len(synth_report)}")
    by_reason: Counter = Counter()
    for flags in synth_report.values():
        for k in flags:
            by_reason[k] += 1
    print(f"synthesis reasons: {dict(by_reason)}")
    if synth_report:
        print("topics needing synthesis:")
        for t, flags in synth_report.items():
            print(f"  - {t}: {', '.join(flags)}")
    sample = get_review_bank("there_is_are")
    print(f"sample there_is_are subtypes: {[x['subtype'] for x in sample]}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
