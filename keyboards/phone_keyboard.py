# keyboards/phone_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для запроса контакта пользователя.
    Содержит кнопки "Поделиться контактом", "Отказаться" и "Назад".
    Клавиатура одноразовая и исчезает после выбора.

    Returns:
        ReplyKeyboardMarkup: Клавиатура для запроса контакта.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Поделиться контактом", request_contact=True),
                KeyboardButton(text="Отказаться"),
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True  # Клавиатура исчезнет после выбора
    )
    return keyboard