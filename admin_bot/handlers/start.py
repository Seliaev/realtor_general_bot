# admin_bot/handlers/start.py
from aiogram import Router, F
from aiogram.types import Message

from admin_bot.keyboards.admin_menu import get_admin_menu
from config import ADMIN_IDS

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    """
    Обработчик команды '/start' для админ-бота.
    Проверяет, является ли пользователь администратором, и отображает админ-панель,
    если права доступа есть, иначе сообщает об отсутствии прав.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            "Добро пожаловать в админ-панель! Выберите действие:",
            reply_markup=get_admin_menu()
        )
    else:
        await message.answer("У вас нет прав доступа к админ-панели.")