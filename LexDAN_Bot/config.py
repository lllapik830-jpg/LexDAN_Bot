import os
from dotenv import load_dotenv

load_dotenv()

# Секреты — никогда не выкладывай их в GitHub открытым текстом.
# На Render их кладут в Environment Variables.
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Username бота без @ — для реф-ссылок (пример: LexDAN_bot)
BOT_USERNAME = (os.getenv("BOT_USERNAME") or "").lstrip("@")

# Контакт поддержки без @ (можно переопределить через SUPPORT_USERNAME в env)
SUPPORT_USERNAME = (os.getenv("SUPPORT_USERNAME") or "lllapik").lstrip("@")

# Файл-«база» пользователей (fallback, если нет DATABASE_URL)
USER_DATA_FILE = "users.json"

# PostgreSQL на Render (Internal/External Database URL)
DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

# Твой Telegram ID — админ-команды (/admin, /grant_*, лотереи…)
MANAGER_ID = int(os.getenv("MANAGER_ID") or "1809897303")

# ЮKassa (оплата подписки + автоплатежи)
YOOKASSA_SHOP_ID = (os.getenv("YOOKASSA_SHOP_ID") or "").strip()
YOOKASSA_SECRET_KEY = (os.getenv("YOOKASSA_SECRET_KEY") or "").strip()
# Публичный HTTPS бота без слэша: https://xxx.onrender.com
# Нужен для HTTP-уведомлений ЮKassa: {PUBLIC_BASE_URL}/yookassa/webhook
PUBLIC_BASE_URL = (os.getenv("PUBLIC_BASE_URL") or "").rstrip("/")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Добавь его в переменные окружения.")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден! Добавь его в переменные окружения.")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY не найден! Добавь его в переменные окружения.")
