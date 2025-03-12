# admin_bot/keyboards/control_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_status

def get_control_keyboard() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для переключения статуса бота (вкл/выкл).
    Текст кнопки зависит от текущего значения bot_status['is_active'].

    Returns:
        InlineKeyboardMarkup: Клавиатура с одной кнопкой ("Переключить" или "Включить").
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Переключить" if bot_status['is_active'] else "Включить",
                callback_data="toggle_bot"
            )
        ]
    ])
    return keyboard