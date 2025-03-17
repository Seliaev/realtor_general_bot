# admin_bot/handlers/control.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging
from utils.logger import logger

from admin_bot.keyboards.control_keyboard import get_control_keyboard
from config import bot_status, ADMIN_IDS, update_bot_status  # Обновленный импорт

router = Router()

@router.message(F.text == "Управление ботом")
async def show_control(message: Message) -> None:
    """
    Обработчик команды 'Управление ботом' для отображения текущего статуса бота.
    Доступно только администраторам, указанным в ADMIN_IDS.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            f"Текущий статус бота: {'Включен' if bot_status['is_active'] else 'Выключен'}",
            reply_markup=get_control_keyboard()
        )

@router.callback_query(F.data.in_({"toggle_bot"}))
async def toggle_bot(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик callback-запроса для переключения статуса бота (вкл/выкл).
    Доступно только администраторам, указанным в ADMIN_IDS.
    Обновляет текст сообщения и клавиатуру после переключения.

    Args:
        callback (CallbackQuery): Объект callback-запроса от инлайн-кнопки.
        state (FSMContext): Контекст состояния FSM (не используется в данном случае).
    """
    if callback.from_user.id in ADMIN_IDS:
        new_status = not bot_status['is_active']
        update_bot_status(new_status)  # Обновляем статус через функцию
        await callback.answer(f"Бот {'включен' if new_status else 'выключен'}")
        await callback.message.edit_text(
            f"Текущий статус бота: {'Включен' if bot_status['is_active'] else 'Выключен'}",
            reply_markup=get_control_keyboard()
        )