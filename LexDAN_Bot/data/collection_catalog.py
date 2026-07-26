"""Каталог коллекции Рико — 15 элементов."""

from __future__ import annotations

import os

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "collection")

RARITY_COMMON = "common"
RARITY_RARE = "rare"
RARITY_VERY_RARE = "very_rare"

RARITY_LABEL_RU = {
    RARITY_COMMON: "Обычный",
    RARITY_RARE: "Редкий",
    RARITY_VERY_RARE: "Очень редкий",
}

# Веса ролла: 60% / 30% / 10%
RARITY_WEIGHTS = (
    (RARITY_COMMON, 60),
    (RARITY_RARE, 30),
    (RARITY_VERY_RARE, 10),
)

COLLECTION_ELEMENTS: list[dict] = [
    {"id": 1, "rarity": RARITY_COMMON, "title_ru": "Привет, Рико", "title_en": "Hello Rico"},
    {"id": 2, "rarity": RARITY_COMMON, "title_ru": "Азбука", "title_en": "ABC Blocks"},
    {"id": 3, "rarity": RARITY_COMMON, "title_ru": "Книжный червь", "title_en": "Bookworm"},
    {"id": 4, "rarity": RARITY_COMMON, "title_ru": "Слушатель", "title_en": "Listener"},
    {"id": 5, "rarity": RARITY_COMMON, "title_ru": "У Big Ben", "title_en": "Big Ben"},
    {"id": 6, "rarity": RARITY_COMMON, "title_ru": "Tea time", "title_en": "Tea Time"},
    {"id": 7, "rarity": RARITY_COMMON, "title_ru": "Заметки", "title_en": "Notes"},
    {"id": 8, "rarity": RARITY_RARE, "title_ru": "Детектив Рико", "title_en": "Detective Rico"},
    {"id": 9, "rarity": RARITY_RARE, "title_ru": "Путешественник", "title_en": "Traveler"},
    {"id": 10, "rarity": RARITY_RARE, "title_ru": "DJ Рико", "title_en": "DJ Rico"},
    {"id": 11, "rarity": RARITY_RARE, "title_ru": "Шеф-повар", "title_en": "Chef Rico"},
    {"id": 12, "rarity": RARITY_RARE, "title_ru": "У моста", "title_en": "Tower Bridge"},
    {"id": 13, "rarity": RARITY_VERY_RARE, "title_ru": "Выпускник", "title_en": "Graduate"},
    {"id": 14, "rarity": RARITY_VERY_RARE, "title_ru": "Grammar Guard", "title_en": "Grammar Guard"},
    {"id": 15, "rarity": RARITY_VERY_RARE, "title_ru": "Король English", "title_en": "King of English"},
]

TOTAL_ELEMENTS = len(COLLECTION_ELEMENTS)


def element_by_id(el_id: int) -> dict | None:
    for e in COLLECTION_ELEMENTS:
        if int(e["id"]) == int(el_id):
            return e
    return None


def elements_by_rarity(rarity: str) -> list[dict]:
    return [e for e in COLLECTION_ELEMENTS if e["rarity"] == rarity]


def asset_path(el_id: int) -> str:
    return os.path.join(_ASSETS, f"el_{int(el_id):02d}.png")
