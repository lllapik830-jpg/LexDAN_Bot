# -*- coding: utf-8 -*-
"""
Развёрнутые рассказы Рико для Grammar B1–C2.
Подключается из grammar_narratives.py поверх коротких версий.
"""

from data.grammar_narr_b1 import NARR_B1
from data.grammar_narr_b2 import NARR_B2
from data.grammar_narr_c1 import NARR_C1
from data.grammar_narr_c2 import NARR_C2

NARRATIVES_B1C2: dict[str, str] = {}
NARRATIVES_B1C2.update(NARR_B1)
NARRATIVES_B1C2.update(NARR_B2)
NARRATIVES_B1C2.update(NARR_C1)
NARRATIVES_B1C2.update(NARR_C2)
