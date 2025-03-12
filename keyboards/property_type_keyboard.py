# keyboards/property_type_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.text_manager import get_text

def get_property_type_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора типа недвижимости.
    Содержит кнопки "Новостройка", "Вторичное жилье", "Исторический центр" и "Назад".
    Тексты кнопок берутся из файла texts/main_menu.yaml.
    Клавиатура одноразовая и исчезает после выбора.

    Returns:
        ReplyKeyboardMarkup: Клавиатура для выбора типа недвижимости.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("main_menu", "new_build")),
                KeyboardButton(text=get_text("main_menu", "secondary"))
            ],
            [
                KeyboardButton(text=get_text("main_menu", "historic")),
                KeyboardButton(text=get_text("main_menu", "back"))
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True  # Клавиатура исчезнет после выбора
    )
    return keyboard