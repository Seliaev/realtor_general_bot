# admin_bot/states/admin_states.py
from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    """
    Класс, определяющий состояния FSM для админ-бота.
    Используется для управления процессом рассылки сообщений.
    """
    SELECT_TYPE = State()  # Выбор типа рассылки (массово/избирательно)
    ENTER_TEXT = State()  # Ввод текста сообщения
    ENTER_USER_ID = State()  # Ввод ID пользователя (для избирательной рассылки)