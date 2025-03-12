# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.text_manager import get_text

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру главного меню бота.
    Содержит кнопки для подбора недвижимости, продажи и записи на экскурсию.
    Тексты кнопок берутся из файла texts/main_menu.yaml.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками главного меню.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("main_menu", "search_property"))],
            [KeyboardButton(text=get_text("main_menu", "sell_property"))],
            [KeyboardButton(text=get_text("main_menu", "excursion"))],
        ],
        resize_keyboard=True
    )
    return keyboard