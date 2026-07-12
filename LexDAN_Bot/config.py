import os
from dotenv import load_dotenv

load_dotenv()

# --- ТОКЕНЫ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# --- ФАЙЛ ДАННЫХ ---
USER_DATA_FILE = "users.json"

# --- ID МЕНЕДЖЕРА (твой Telegram ID) ---
MANAGER_ID = 1809897303  # Замени на свой ID

# --- ПРОВЕРКА КЛЮЧЕЙ ---
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Добавь его в переменные окружения.")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден! Добавь его в переменные окружения.")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY не найден! Добавь его в переменные окружения.")