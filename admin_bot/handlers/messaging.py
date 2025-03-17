# admin_bot/handlers/messaging.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from admin_bot.keyboards.messaging_keyboard import get_messaging_keyboard
from utils.logger import logger
from utils.database import db
from config import BOT_TOKEN, ADMIN_IDS
import re

router = Router()

# Состояния для FSM
class MessagingStates(StatesGroup):
    SELECT_TYPE = State()  # Выбор типа рассылки (массово/избирательно)
    ENTER_TEXT = State()  # Ввод текста сообщения
    ENTER_USER_ID = State()  # Ввод ID пользователя (для избирательной рассылки)
    ADD_BUTTONS = State()  # Дополнительный шаг для добавления кнопок (опционально)
    ENTER_BUTTON_TEXT = State()  # Ввод текста кнопки
    ENTER_BUTTON_URL = State()  # Ввод URL кнопки

async def send_message_to_user(main_bot: Bot, user_id: int, text: str, reply_markup: InlineKeyboardMarkup = None) -> None:
    """
    Асинхронная функция для отправки сообщения пользователю от имени основного бота с поддержкой кнопок.

    Args:
        main_bot (Bot): Экземпляр бота с токеном основного бота.
        user_id (int): ID получателя.
        text (str): Текст сообщения (с HTML-форматированием).
        reply_markup (InlineKeyboardMarkup, optional): Клавиатура с кнопками.
    """
    try:
        await main_bot.send_message(user_id, text, parse_mode="HTML", reply_markup=reply_markup)
        logger.info(f"Сообщение отправлено пользователю {user_id} от основного бота")
    except Exception as e:
        logger.error(f"Ошибка отправки пользователю {user_id}: {str(e)}")

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
        await state.update_data(main_bot_token=BOT_TOKEN)  # Сохраняем токен основного бота
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
    await callback.message.edit_text("Введите текст сообщения (можно использовать HTML, например, <b>жирный</b>):")

@router.message(MessagingStates.ENTER_TEXT)
async def enter_text(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода текста сообщения для рассылки.
    Сохраняет текст и предлагает добавить кнопки, либо переходит к рассылке.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.update_data(text=message.text)
    await state.set_state(MessagingStates.ADD_BUTTONS)
    await message.answer("Хотите добавить кнопки? (да/нет)")

@router.message(MessagingStates.ADD_BUTTONS, F.text.lower().in_({"да", "нет"}))
async def add_buttons(message: Message, state: FSMContext) -> None:
    """
    Обработчик выбора добавления кнопок.
    Если 'да', запрашивает текст и URL кнопки, если 'нет', запускает рассылку.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    data = await state.get_data()
    text = data["text"]
    main_bot_token = data.get("main_bot_token")
    main_bot = Bot(token=main_bot_token)

    if message.text.lower() == "да":
        await state.update_data(button_text="", button_url="")
        await state.set_state(MessagingStates.ENTER_BUTTON_TEXT)
        await message.answer("Введите текст для кнопки:")
    else:
        users = await db.get_all_users()
        if users:
            for user_id in users:
                await send_message_to_user(main_bot, user_id, text)
        await message.answer("Массовое сообщение отправлено (проверьте логи).")
        await state.clear()

@router.message(MessagingStates.ENTER_BUTTON_TEXT)
async def enter_button_text(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода текста кнопки.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.update_data(button_text=message.text)
    await state.set_state(MessagingStates.ENTER_BUTTON_URL)
    await message.answer("Введите URL для кнопки (укажите полный адрес с https:// или http://):")

@router.message(MessagingStates.ENTER_BUTTON_URL)
async def enter_button_url(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода URL кнопки и выполнения рассылки.
    Добавляет https://, если протокол отсутствует.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    data = await state.get_data()
    text = data["text"]
    button_text = data["button_text"]
    button_url = message.text

    # Добавляем https://, если протокол отсутствует
    if not re.match(r'^https?://', button_url, re.IGNORECASE):
        button_url = f"https://{button_url}"

    main_bot_token = data.get("main_bot_token")
    main_bot = Bot(token=main_bot_token)

    # Создаем инлайн-кнопку
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, url=button_url)]
    ])

    users = await db.get_all_users()
    if users:
        for user_id in users:
            await send_message_to_user(main_bot, user_id, text, keyboard)
    await message.answer("Массовое сообщение с кнопкой отправлено (проверьте логи).")
    await state.clear()

@router.message(MessagingStates.ENTER_TEXT, ~F.text.lower().in_({"да", "нет"}))
async def invalid_add_buttons(message: Message, state: FSMContext) -> None:
    """
    Обработчик некорректного ответа на вопрос о кнопках.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await message.answer("Пожалуйста, ответьте 'да' или 'нет'.")

@router.message(MessagingStates.ENTER_USER_ID)
async def enter_user_id(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода ID пользователя для избирательной рассылки.
    Отправляет сообщение указанному пользователю.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    data = await state.get_data()
    user_id = message.text
    text = data["text"]
    main_bot_token = data.get("main_bot_token")
    main_bot = Bot(token=main_bot_token)
    try:
        await send_message_to_user(main_bot, int(user_id), text)
    except Exception as e:
        logger.error(f"Ошибка отправки пользователю {user_id}: {str(e)}")
    await message.answer(f"Сообщение '{text}' отправлено пользователю с ID {user_id} (проверьте логи).")
    await state.clear()