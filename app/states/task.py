from aiogram.fsm.state import State, StatesGroup

class CreateTaskState(StatesGroup):
    new_task = State()
    read_title = State()
    read_description = State()