# admin_bot/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.text_manager import get_text

def get_admin_menu() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру главного меню админ-панели с кнопками управления и рассылки.
    Тексты берутся из файла texts/admin_menu.yaml.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками "Управление ботом" и "Рассылка".
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("admin_menu", "control"))],
            [KeyboardButton(text=get_text("admin_menu", "messaging"))],
        ],
        resize_keyboard=True
    )
    return keyboard