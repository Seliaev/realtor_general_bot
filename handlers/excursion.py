# handlers/excursion.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from utils.logger import logger

from keyboards.main_menu import get_main_menu
from keyboards.phone_keyboard import get_phone_keyboard
from utils.notify_admin import notify_admins
from utils.text_manager import get_text
from utils.google_sheets import append_row
from states.excursion_states import ExcursionStates

router = Router()

@router.message(F.text == get_text("main_menu", "excursion"))
async def start_excursion(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды для записи на экскурсию.
    Устанавливает состояние phone и запрашивает контакт пользователя.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.set_state(ExcursionStates.phone)
    await message.answer("Поделитесь контактом и мы поможем Вам", reply_markup=get_phone_keyboard())

@router.message(ExcursionStates.phone, F.content_type.in_({"contact", "text"}))
async def process_excursion(message: Message, state: FSMContext) -> None:
    """
    Обработчик получения контакта или отказа для записи на экскурсию.
    Сохраняет данные в Google Sheets и отправляет уведомление админам, либо возвращает в главное меню при нажатии 'Отмена'.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.text == get_text("main_menu", "cancel"):
        logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе записи на экскурсию, возвращаю в главное меню")
        await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
        await state.clear()
        return
    phone = message.contact.phone_number if message.content_type == "contact" else None
    success = append_row("ExcursionRequests", [phone if phone else "Отказался",
                                              f"{message.from_user.username}.t.me" if message.from_user.username else "Скрыт",])
    if success:
        notification_text = (f"<b>Новая заявка от бота\n</b>"
                            f"Заявка на экскурсию:\nТелефон: {phone if phone else 'Не указан'}\n"
                            f"Telegram: @{message.from_user.username if message.from_user.username else 'Скрыт'}")
        await notify_admins(notification_text)
    await message.answer(
        get_text("responses", "success" if success else "error"),
        reply_markup=get_main_menu()
    )
    await state.clear()