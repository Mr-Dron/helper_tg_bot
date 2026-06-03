from aiogram.fsm.state import State, StatesGroup

class CreateProfileState(StatesGroup):
    new_company = State()
    