# handlers/property_sell.py
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import get_main_menu
from keyboards.phone_keyboard import get_phone_keyboard
from utils.notify_admin import notify_admins
from utils.text_manager import get_text
from utils.google_sheets import append_row
from states.sell_states import SellStates

router = Router()

class SellStates(StatesGroup):
    """
    Класс, определяющий состояния FSM для процесса продажи недвижимости.
    """
    phone = State()  # Поделиться контактом или отказ

@router.message(F.text == get_text("main_menu", "sell_property"))
async def start_sell(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды для начала процесса подачи заявки на продажу.
    Устанавливает состояние phone и запрашивает контакт пользователя.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.set_state(SellStates.phone)
    await message.answer("Поделитесь контактом и мы поможем Вам", reply_markup=get_phone_keyboard())

@router.message(SellStates.phone, F.content_type.in_({"contact", "text"}))
async def process_sell(message: Message, state: FSMContext) -> None:
    """
    Обработчик получения контакта или отказа для заявки на продажу.
    Сохраняет данные в Google Sheets и отправляет уведомление админам.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    phone = message.contact.phone_number if message.content_type == "contact" else None
    success = append_row("SellRequests", [phone if phone else "Отказался",
                                                                f"{message.from_user.username}.t.me" if message.from_user.username else "Скрыт",])
    if success:
        notification_text = (f"<b>Новая заявка от бота\n</b>"
                             f"Заявка на продажу:\n"
                             f"Телефон: {phone if phone else 'Не указан'}\n"
                             f"Telegram: @{message.from_user.username if message.from_user.username else 'Скрыт'}")
        await notify_admins(notification_text)
    await message.answer(
        get_text("responses", "success" if success else "error"),
        reply_markup=get_main_menu()
    )
    await state.clear()