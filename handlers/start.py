# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import logging
from utils.logger import logger

from keyboards.main_menu import get_main_menu
from utils.text_manager import get_text
from utils.database import db

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды '/start' для основного бота.
    Отправляет приветственное сообщение с изображением, открывает главное меню и регистрирует пользователя, если он еще не зарегистрирован.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    # Регистрируем пользователя в базе данных
    if not await db.register_user(message.from_user.id):
        logger.error(f"Не удалось зарегистрировать пользователя {message.from_user.id}")
    else:
        logger.info(f"Пользователь {message.from_user.id} успешно обработан в базе данных")

    photo = FSInputFile("pic/7694cf01-b877-4a89-be7a-3c1c3db2ff13.jpg")
    await message.answer_photo(
        photo=photo,
        caption=get_text("welcome", "greeting"),
        reply_markup=get_main_menu()
    )

@router.message(F.text == get_text("main_menu", "cancel"))
async def process_cancel(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды 'Отмена' для возврата в главное меню.
    Очищает текущее состояние и возвращает главное меню.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.clear()
    await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())