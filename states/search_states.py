# states/search_states.py
from aiogram.fsm.state import State, StatesGroup

class SearchStates(StatesGroup):
    """
    Класс, определяющий состояния FSM для процесса подбора недвижимости.
    """
    property_type = State()  # Выбор типа недвижимости (новостройка, вторичка, исторический центр)
    rooms = State()         # Выбор количества комнат
    district = State()      # Выбор района
    budget = State()        # Указание бюджета
    condition = State()     # Выбор состояния (только для исторического центра)
    phone = State()         # Поделиться контактом или отказ