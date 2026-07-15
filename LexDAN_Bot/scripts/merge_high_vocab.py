"""Собрать A2–C2 банки и влить в vocabulary_words / vocabulary_phrases."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.vocabulary_words import WORDS as A0A1_WORDS, _e
from data.build_vocab_banks_high import A2_RAW
from data._vocab_high_b1_c2 import B1_RAW, B2_RAW, C1_RAW, C2_RAW, PHRASES_RAW


def pack(items: list[tuple[str, str, str]]) -> list[dict]:
    return [_e(en, ru, em) for en, ru, em in items]


def dedupe(items: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[str] = set()
    out = []
    for en, ru, em in items:
        k = en.strip().lower()
        if k in seen or not en.strip():
            continue
        seen.add(k)
        out.append((en.strip(), ru.strip(), em.strip()))
    return out


def existing_en() -> set[str]:
    s: set[str] = set()
    for topics in A0A1_WORDS.values():
        for words in topics.values():
            for w in words:
                s.add(w["en"].strip().lower())
    return s


def filter_new(items, known: set[str]) -> list[tuple[str, str, str]]:
    out = []
    for en, ru, em in items:
        k = en.lower()
        if k in known:
            continue
        known.add(k)
        out.append((en, ru, em))
    return out


def build_words() -> dict:
    known = existing_en()
    raw_all = {"A2": A2_RAW, "B1": B1_RAW, "B2": B2_RAW, "C1": C1_RAW, "C2": C2_RAW}
    result = {}
    for level, topics in raw_all.items():
        result[level] = {}
        for topic, raw in topics.items():
            items = dedupe(list(raw))
            # сперва без пересечений с A0/A1 и другими темами upper
            clean = filter_new(items, known)
            # если мало — добираем локальные (уже известные в known снимаем только global A0A1)
            if len(clean) < 30:
                a0a1 = existing_en()
                local_known = set(a0a1)
                # allow reuse across upper levels only if short
                clean2 = []
                for en, ru, em in items:
                    k = en.lower()
                    if k in a0a1:
                        continue
                    if k in {x[0].lower() for x in clean2}:
                        continue
                    local_known.add(k)
                    clean2.append((en, ru, em))
                clean = clean2
                for en, _, _ in clean:
                    known.add(en.lower())
            if len(clean) < 28:
                print(f"WARN {level}/{topic}: only {len(clean)}")
            result[level][topic] = pack(clean[:45])
            print(f"OK {level}/{topic}: {len(result[level][topic])}")
    return result


def build_phrases() -> dict:
    result = {}
    for level, topics in PHRASES_RAW.items():
        result[level] = {}
        for topic, raw in topics.items():
            items = dedupe(list(raw))
            if len(items) < 10:
                print(f"WARN phrases {level}/{topic}: {len(items)}")
            result[level][topic] = pack(items[:15])
            print(f"PHR {level}/{topic}: {len(result[level][topic])}")
    return result


def inject_into_words(high: dict) -> None:
    path = ROOT / "data" / "vocabulary_words.py"
    text = path.read_text(encoding="utf-8")
    # strip old high-level keys if re-running
    marker = "\n# === HIGH_LEVELS_START ===\n"
    if marker in text:
        before = text.split(marker)[0]
        # keep helpers after WORDS closing - rebuild from A0A1 structure
        text = before
    # Find WORDS closing `}` before has_vocabulary_level
    idx = text.find("\ndef has_vocabulary_level")
    if idx < 0:
        raise SystemExit("cannot find has_vocabulary_level")
    head = text[:idx].rstrip()
    # head should end with `}` of WORDS - remove trailing `}\n`
    if not head.endswith("}"):
        raise SystemExit("WORDS dict shape unexpected")
    # remove final } of WORDS dict
    head = head[:-1].rstrip()
    if head.endswith(","):
        pass
    else:
        head += ","

    lines = [head, "", marker.rstrip(), "# auto A2–C2"]
    for level in ("A2", "B1", "B2", "C1", "C2"):
        lines.append(f'    "{level}": {{')
        for topic, words in high[level].items():
            lines.append(f'        "{topic}": [')
            for w in words:
                en = w["en"].replace("\\", "\\\\").replace('"', '\\"')
                ru = w["ru"].replace("\\", "\\\\").replace('"', '\\"')
                em = w["emoji"].replace("\\", "\\\\").replace('"', '\\"')
                lines.append(f'            _e("{en}", "{ru}", "{em}"),')
            lines.append("        ],")
        lines.append("    },")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def has_vocabulary_level(level: str) -> bool:")
    lines.append("    return level in WORDS and bool(WORDS[level])")
    lines.append("")
    lines.append("")
    lines.append("def get_words(level: str, topic_id: str) -> list[dict]:")
    lines.append("    return list(WORDS.get(level, {}).get(topic_id, []))")
    lines.append("")
    lines.append("")
    lines.append("def get_word_entry(level: str, topic_id: str, en: str) -> dict | None:")
    lines.append('    key = (en or "").strip().lower()')
    lines.append("    for w in get_words(level, topic_id):")
    lines.append('        if w["en"].lower() == key:')
    lines.append("            return w")
    lines.append("    return None")
    lines.append("")
    lines.append("")
    lines.append("def words_total(level: str, topic_id: str) -> int:")
    lines.append("    return len(get_words(level, topic_id))")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {path}")


def inject_into_phrases(high: dict) -> None:
    path = ROOT / "data" / "vocabulary_phrases.py"
    text = path.read_text(encoding="utf-8")
    marker = "\n# === HIGH_PHRASES_START ===\n"
    if marker in text:
        text = text.split(marker)[0]
    idx = text.find("\ndef has_vocabulary_level")
    if idx < 0:
        raise SystemExit("phrases: cannot find helper")
    head = text[:idx].rstrip()
    if not head.endswith("}"):
        raise SystemExit("PHRASES shape unexpected")
    head = head[:-1].rstrip()
    if not head.endswith(","):
        head += ","

    lines = [head, "", marker.rstrip()]
    for level in ("A2", "B1", "B2", "C1", "C2"):
        if level not in high:
            continue
        lines.append(f'    "{level}": {{')
        for topic, phrases in high[level].items():
            lines.append(f'        "{topic}": [')
            for p in phrases:
                en = p["en"].replace("\\", "\\\\").replace('"', '\\"')
                ru = p["ru"].replace("\\", "\\\\").replace('"', '\\"')
                em = p["emoji"].replace("\\", "\\\\").replace('"', '\\"')
                lines.append(f'            _p("{en}", "{ru}", "{em}"),')
            lines.append("        ],")
        lines.append("    },")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def has_vocabulary_level(level: str) -> bool:")
    lines.append("    return level in PHRASES and bool(PHRASES[level])")
    lines.append("")
    lines.append("")
    lines.append("def get_phrases(level: str, topic_id: str) -> list[dict]:")
    lines.append("    return list(PHRASES.get(level, {}).get(topic_id, []))")
    lines.append("")
    lines.append("")
    lines.append("def get_phrase_entry(level: str, topic_id: str, en: str) -> dict | None:")
    lines.append('    key = (en or "").strip().lower()')
    lines.append("    for p in get_phrases(level, topic_id):")
    lines.append('        if p["en"].lower() == key:')
    lines.append("            return p")
    lines.append("    return None")
    lines.append("")
    lines.append("")
    lines.append("def phrases_total(level: str, topic_id: str) -> int:")
    lines.append("    return len(get_phrases(level, topic_id))")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {path}")


def main():
    words = build_words()
    phrases = build_phrases()
    inject_into_words(words)
    inject_into_phrases(phrases)
    # summary
    for lv in ("A2", "B1", "B2", "C1", "C2"):
        tw = sum(len(v) for v in words[lv].values())
        tp = sum(len(v) for v in phrases.get(lv, {}).values())
        print(f"{lv}: {tw} words, {tp} phrases")


if __name__ == "__main__":
    main()
