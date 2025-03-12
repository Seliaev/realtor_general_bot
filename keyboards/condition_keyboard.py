#keyboards/condition_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_condition_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Под ремонт"),
                KeyboardButton(text="С ремонтом")
            ],
            [
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard