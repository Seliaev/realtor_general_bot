# states/excursion_states.py
from aiogram.fsm.state import State, StatesGroup

class ExcursionStates(StatesGroup):
    """
    Класс, определяющий состояния FSM для процесса записи на экскурсию.
    """
    phone = State()  # Поделиться контактом или отказ