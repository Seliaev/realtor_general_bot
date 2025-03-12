# config.py
from environs import Env
from typing import List, Dict
import os
import logging
from utils.logger import logger

env = Env()
# Проверка наличия файла .env
if not os.path.exists(".env"):
    message = "Файл .env не найден в корне проекта. Пожалуйста, создайте его и добавьте необходимые переменные."
    print(message)
    logger.error(message)
    exit(1)

env.read_env()

# Проверка наличия всех необходимых переменных
required_vars = ["BOT_TOKEN", "ADMIN_BOT_TOKEN", "ADMIN_IDS", "GOOGLE_SHEET_ID"]
missing_vars = [var for var in required_vars if env(var, default=None) is None]  # Исправленная строка
if missing_vars:
    message = f"Отсутствуют следующие переменные в .env: {', '.join(missing_vars)}. Пожалуйста, добавьте их."
    print(message)
    logger.error(message)
    exit(1)

BOT_TOKEN: str = env.str("BOT_TOKEN")
"""Токен основного бота, загружаемый из файла .env."""
ADMIN_BOT_TOKEN: str = env.str("ADMIN_BOT_TOKEN")
"""Токен админ-бота, загружаемый из файла .env."""
ADMIN_IDS: List[int] = env.list("ADMIN_IDS", subcast=int)
"""Список ID администраторов, загружаемый из файла .env и преобразованный в целые числа."""
GOOGLE_SHEET_ID: str = env.str("GOOGLE_SHEET_ID")
"""ID Google Sheets таблицы, загружаемый из файла .env."""
bot_status: Dict[str, bool] = {"is_active": True}
"""Словарь для хранения статуса бота, где 'is_active' указывает, включен ли бот."""