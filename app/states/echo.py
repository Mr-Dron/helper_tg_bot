from aiogram.fsm.state import State, StatesGroup

class EchoState(StatesGroup):
    active = State()