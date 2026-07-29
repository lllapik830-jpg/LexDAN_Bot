"""
Корень репо: не запускай polling отсюда отдельно.
Рабочий бот: LexDAN_Bot/main.py (Root Directory на Render = LexDAN_Bot).
"""

import runpy
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent / "LexDAN_Bot"
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if __name__ == "__main__":
    runpy.run_path(str(_ROOT / "main.py"), run_name="__main__")
