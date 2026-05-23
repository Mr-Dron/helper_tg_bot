from aiogram.fsm.state import State, StatesGroup

class UpdateProfileState(StatesGroup):
    waiting_for_firstname = State()
    waiting_for_username = State()
    waiting_for_telegramlink = State()

    