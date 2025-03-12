# handlers/callback_handlers.py
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.property_search import PropertySearch
from keyboards.rooms_keyboard import get_rooms_keyboard
from states.search_states import SearchStates



router = Router()

@router.callback_query(PropertySearch.property_type)
async def process_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик callback-запроса для выбора типа недвижимости.
    Сохраняет выбранный тип в состоянии, удаляет предыдущее сообщение и запрашивает выбор количества комнат.

    Args:
        callback (CallbackQuery): Объект callback-запроса от инлайн-кнопки.
        state (FSMContext): Контекст состояния FSM для управления процессом.
    """
    await state.update_data(property_type=callback.data)
    await state.set_state(SearchStates.rooms)
    await callback.message.delete()
    await callback.message.answer("Выберите количество комнат:", reply_markup=get_rooms_keyboard())
    await callback.answer()