# keyboards/rooms_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_rooms_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора количества комнат.
    Содержит кнопки "1", "2", "3", "4+" и кнопку "Назад".

    Returns:
        ReplyKeyboardMarkup: Клавиатура для выбора количества комнат.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1"),
                KeyboardButton(text="2"),
                KeyboardButton(text="3")
            ],
            [
                KeyboardButton(text="4+"),
                KeyboardButton(text="Отмена")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard