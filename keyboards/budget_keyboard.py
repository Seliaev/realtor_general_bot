# keyboards/budget_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_budget_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора бюджета недвижимости.
    Предоставляет четыре диапазона бюджета и кнопку "Назад".

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками выбора бюджета.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="До 5 млн"),
                KeyboardButton(text="5-10 млн")
            ],
            [
                KeyboardButton(text="10-20 млн"),
                KeyboardButton(text="20+ млн"),
                KeyboardButton(text="Отмена")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard