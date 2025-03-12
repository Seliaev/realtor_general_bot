# keyboards/district_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_district_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора района недвижимости.
    Предоставляет пять вариантов районов и кнопку "Назад".

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками выбора района.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Центр"),
                KeyboardButton(text="Север"),
                KeyboardButton(text="Юг")
            ],
            [
                KeyboardButton(text="Восток"),
                KeyboardButton(text="Запад"),
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard