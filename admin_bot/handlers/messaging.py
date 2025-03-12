# admin_bot/handlers/messaging.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_IDS
from admin_bot.keyboards.messaging_keyboard import get_messaging_keyboard

router = Router()

# Состояния для FSM
class MessagingStates(StatesGroup):
    SELECT_TYPE = State()  # Выбор типа рассылки (массово/избирательно)
    ENTER_TEXT = State()  # Ввод текста сообщения
    ENTER_USER_ID = State()  # Ввод ID пользователя (для избирательной рассылки)

@router.message(F.text == "Рассылка")
async def start_messaging(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды 'Рассылка' для начала процесса отправки сообщений.
    Доступно только администраторам, указанным в ADMIN_IDS.
    Устанавливает состояние SELECT_TYPE и отображает клавиатуру для выбора типа рассылки.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.from_user.id in ADMIN_IDS:
        await state.set_state(MessagingStates.SELECT_TYPE)
        await message.answer(
            "Выберите тип рассылки:",
            reply_markup=get_messaging_keyboard()
        )

@router.callback_query(F.data.in_({"mass", "selective"}))
async def select_messaging_type(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик callback-запроса для выбора типа рассылки (массово/избирательно).
    Сохраняет выбранный тип и переходит к вводу текста сообщения.

    Args:
        callback (CallbackQuery): Объект callback-запроса от инлайн-кнопки.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.update_data(messaging_type=callback.data)
    await state.set_state(MessagingStates.ENTER_TEXT)
    await callback.answer()
    await callback.message.edit_text("Введите текст сообщения:")

@router.message(MessagingStates.ENTER_TEXT)
async def enter_text(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода текста сообщения для рассылки.
    Сохраняет текст и, в зависимости от типа рассылки, либо запрашивает ID пользователя (для избирательной),
    либо завершает процесс (для массовой, пока симуляция).

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.update_data(text=message.text)
    data = await state.get_data()
    if data["messaging_type"] == "selective":
        await state.set_state(MessagingStates.ENTER_USER_ID)
        await message.answer("Введите ID пользователя для отправки:")
    else:
        await message.answer("Массовое сообщение будет отправлено всем пользователям (пока симуляция).")
        await state.clear()

@router.message(MessagingStates.ENTER_USER_ID)
async def enter_user_id(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода ID пользователя для избирательной рассылки.
    Завершает процесс, симулируя отправку сообщения указанному пользователю.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    data = await state.get_data()
    user_id: str = message.text
    text: str = data["text"]
    await message.answer(f"Сообщение '{text}' отправлено пользователю с ID {user_id} (симуляция).")
    await state.clear()