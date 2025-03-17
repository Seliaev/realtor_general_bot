# handlers/property_search.py
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from utils.logger import logger

from keyboards.budget_keyboard import get_budget_keyboard
from keyboards.condition_keyboard import get_condition_keyboard
from keyboards.district_keyboard import get_district_keyboard
from keyboards.main_menu import get_main_menu
from keyboards.phone_keyboard import get_phone_keyboard
from keyboards.rooms_keyboard import get_rooms_keyboard
from keyboards.property_type_keyboard import get_property_type_keyboard
from utils.text_manager import get_text
from utils.google_sheets import append_row
from utils.notify_admin import notify_admins

router = Router()

class PropertySearch(StatesGroup):
    """
    Класс, определяющий состояния FSM для процесса подбора недвижимости.
    """
    property_type = State()  # Выбор типа недвижимости (новостройка, вторичка, исторический центр)
    rooms = State()         # Выбор количества комнат
    district = State()      # Выбор района
    budget = State()        # Указание бюджета
    condition = State()     # Выбор состояния (только для исторического центра)
    phone = State()         # Поделиться контактом или отказ

@router.message(F.text == get_text("main_menu", "search_property"))
async def start_search(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды для начала процесса подбора недвижимости.
    Устанавливает состояние property_type и отображает клавиатуру для выбора типа.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.set_state(PropertySearch.property_type)
    await message.answer(
        "Выберите тип недвижимости:",
        reply_markup=get_property_type_keyboard()
    )

# Новый роутер для обработки "Отмена" на этапе property_type
@router.message(PropertySearch.property_type, F.text == get_text("main_menu", "cancel"))
async def cancel_property_type(message: Message, state: FSMContext) -> None:
    """
    Обработчик нажатия 'Отмена' на этапе выбора типа недвижимости.
    Возвращает в главное меню и очищает состояние.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе выбора типа, возвращаю в главное меню")
    await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
    await state.clear()

@router.message(PropertySearch.property_type, F.text.in_([
    get_text("main_menu", "new_build"),
    get_text("main_menu", "secondary"),
    get_text("main_menu", "historic")
]))
async def process_property_type(message: Message, state: FSMContext) -> None:
    """
    Обработчик выбора типа недвижимости.
    Сохраняет выбранный тип и переходит к выбору количества комнат.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    property_type = message.text
    await state.update_data(property_type=property_type)
    await state.set_state(PropertySearch.rooms)
    await message.answer("Выберите количество комнат:", reply_markup=get_rooms_keyboard())

@router.message(PropertySearch.rooms, F.text)
async def process_rooms(message: Message, state: FSMContext) -> None:
    """
    Обработчик выбора количества комнат.
    Сохраняет выбор и переходит к выбору района, либо возвращает в главное меню при нажатии 'Отмена'.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.text == get_text("main_menu", "cancel"):
        logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе выбора комнат, возвращаю в главное меню")
        await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
        await state.clear()
        return
    await state.update_data(rooms=message.text)
    await state.set_state(PropertySearch.district)
    await message.answer("Выберите район:", reply_markup=get_district_keyboard())

@router.message(PropertySearch.district, F.text)
async def process_district(message: Message, state: FSMContext) -> None:
    """
    Обработчик выбора района.
    Сохраняет выбор и переходит к указанию бюджета, либо возвращает в главное меню при нажатии 'Отмена'.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.text == get_text("main_menu", "cancel"):
        logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе выбора района, возвращаю в главное меню")
        await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
        await state.clear()
        return
    await state.update_data(district=message.text)
    await state.set_state(PropertySearch.budget)
    await message.answer("Укажите бюджет:", reply_markup=get_budget_keyboard())

@router.message(PropertySearch.budget, F.text)
async def process_budget(message: Message, state: FSMContext) -> None:
    """
    Обработчик указания бюджета.
    Сохраняет бюджет и переходит к следующему шагу (состояние или телефон), либо возвращает в главное меню при нажатии 'Отмена'.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.text == get_text("main_menu", "cancel"):
        logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе выбора бюджета, возвращаю в главное меню")
        await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
        await state.clear()
        return
    await state.update_data(budget=message.text)
    data = await state.get_data()
    if data["property_type"] == get_text("main_menu", "historic"):
        await state.set_state(PropertySearch.condition)
        await message.answer("Выберите состояние:", reply_markup=get_condition_keyboard())
    else:
        await state.set_state(PropertySearch.phone)
        await message.answer("Поделитесь контактом или откажитесь:", reply_markup=get_phone_keyboard())

@router.message(PropertySearch.condition, F.text)
async def process_condition(message: Message, state: FSMContext) -> None:
    """
    Обработчик выбора состояния (для исторического центра).
    Сохраняет выбор и переходит к запросу телефона, либо возвращает в главное меню при нажатии 'Отмена'.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.text == get_text("main_menu", "cancel"):
        logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе выбора состояния, возвращаю в главное меню")
        await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
        await state.clear()
        return
    await state.update_data(condition=message.text)
    await state.set_state(PropertySearch.phone)
    await message.answer("Поделитесь контактом и мы поможем Вам", reply_markup=get_phone_keyboard())

@router.message(PropertySearch.phone, F.content_type.in_({"contact", "text"}))
async def process_phone(message: Message, state: FSMContext) -> None:
    """
    Обработчик получения контакта или отказа.
    Сохраняет данные в Google Sheets и отправляет уведомление админам, либо возвращает в главное меню при нажатии 'Отмена'.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    if message.text == get_text("main_menu", "cancel"):
        logger.info(f"Пользователь {message.from_user.id} нажал 'Отмена' на этапе ввода телефона, возвращаю в главное меню")
        await message.answer("Возврат в главное меню.", reply_markup=get_main_menu())
        await state.clear()
        return
    phone = message.contact.phone_number if message.content_type == "contact" else None
    await state.update_data(phone=phone if phone else "Отказался")
    data = await state.get_data()
    row_data = [
        data.get("property_type", ""),
        data.get("rooms", ""),
        data.get("district", ""),
        data.get("budget", ""),
        data.get("condition", ""),
        data.get("phone", ""),
        f"{message.from_user.username}.t.me"
    ]

    success = append_row("SearchRequests", row_data)
    if success:
        notification_text = (f"<b>Новая заявка от бота\n</b>"
                             f"Заявка на подбор:\nТип: {data.get('property_type')}\n"
                             f"Комнаты: {data.get('rooms')}\n"
                             f"Район: {data.get('district')}\n"
                             f"Бюджет: {data.get('budget')}\n"
                             f"Состояние: {data.get('condition') if data.get('condition') else '-'}\n"
                             f"Телефон: {data.get('phone', 'Не указан')}\n"
                             f"Telegram: @{message.from_user.username if message.from_user.username else 'Скрыт'}")
        await notify_admins(notification_text)
    await message.answer(
        get_text("responses", "success" if success else "error"),
        reply_markup=get_main_menu()
    )
    await state.clear()