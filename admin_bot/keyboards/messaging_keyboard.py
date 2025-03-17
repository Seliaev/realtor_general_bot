# admin_bot/keyboards/messaging_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_messaging_keyboard() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для выбора типа рассылки (массово или избирательно).

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками "Массово" и "Избирательно".
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Массово", callback_data="mass")
            #InlineKeyboardButton(text="Избирательно", callback_data="selective")
        ]
    ])
    return keyboard