from aiogram.fsm.state import State, StatesGroup

class CreateDepartment(StatesGroup):
    edit_name = State()
    