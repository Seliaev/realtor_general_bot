# states/sell_states.py
from aiogram.fsm.state import State, StatesGroup

class SellStates(StatesGroup):
    """
    Класс, определяющий состояния FSM для процесса подачи заявки на продажу недвижимости.
    """
    phone = State()  # Поделиться контактом или отказ