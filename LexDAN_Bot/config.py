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

# Файл-«база» пользователей (лежит в корне проекта)
USER_DATA_FILE = "users.json"

# Твой Telegram ID (пригодится для админ-команд позже)
MANAGER_ID = 1809897303

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Добавь его в переменные окружения.")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден! Добавь его в переменные окружения.")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY не найден! Добавь его в переменные окружения.")
