from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users
from app.keyboards import task as task_key
from app.repositories import task as task_rep
from app.services import task as task_ser
from app.states import task as task_state

router = Router()

# region меню задач

@router.callback_query(F.data == "company_tasks")
async def get_company_tasks(callback: CallbackQuery,
                            state: FSMContext,
                            db: AsyncSession):

    data = await state.get_data()
    company_id = data.get("company_id")

    text, keyboard = await task_ser.build_task_menu_context(
        company_id=company_id,
        current_page=1,
        db=db
    )

    await state.update_data(current_page=1)

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )

@router.callback_query(F.data.in_({"page_tasks_previous", "page_tasks_next"}))
async def page_company_tasks(callback: CallbackQuery,
                             state: FSMContext,
                             db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")
    current_page = data.get("current_page")

    if "next" in callback.data:
        current_page += 1
    elif "previous" in callback.data:
        current_page -= 1

    text, keyboard = await task_ser.build_task_menu_context(
        company_id=company_id,
        current_page=current_page,
        db=db
    )

    await state.update_data(current_page=current_page)

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )

# endregion

# region создание задач

@router.callback_query(F.data == "create_task")
async def create_task(callback: CallbackQuery,
                      state: FSMContext):
    
    await state.set_state(task_state.CreateTaskState.new_task)

    text, keyboard = await task_ser.build_task_create_context()

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )

@router.callback_query(task_state.CreateTaskState.new_task,
                       F.data.in_({"edit_title", "edit_description"}))
async def edit_new_task_data(callback: CallbackQuery,
                             state: FSMContext):
    
    if callback.data == "edit_title":
        text = "Введите название задачи"
        await state.set_state(task_state.CreateTaskState.read_title)
    else:
        text = "Введите описание задачи"
        await state.set_state(task_state.CreateTaskState.read_description)

    await callback.message.answer(
        text=text
    )

@router.message(
    task_state.CreateTaskState.read_title
)
async def read_title(message: Message,
                     state: FSMContext):
    
    await state.update_data(title=message.text)
    await state.set_state(task_state.CreateTaskState.new_task)

    data = await state.get_data()
    description = data.get("description")

    text, keyboard = await task_ser.build_task_create_context(title=message.text,
                                                              description=description)

    await message.answer(
        text=text,
        reply_markup=keyboard
    )

@router.message(
    task_state.CreateTaskState.read_description
)
async def read_description(message: Message,
                           state: FSMContext):
    
    await state.update_data(description=message.text)
    await state.set_state(task_state.CreateTaskState.new_task)

    data = await state.get_data()
    title = data.get("title")

    text, keyboard = await task_ser.build_task_create_context(description=message.text,
                                                              title=title)

    await message.answer(
        text=text,
        reply_markup=keyboard
    )

@router.callback_query(F.data.in_({"save_new_task", "inactive_save_task"}))
async def save_new_task(callback: CallbackQuery,
                        state: FSMContext,
                        user: Users,
                        db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")
    title = data.get("title")
    description = data.get("description")

    if callback.data == "inactive_save_task":
        await callback.message.answer(text="Заполните поля")
        text, keyboard = await task_ser.build_task_create_context(description=description,
                                                                  title=title)

        await callback.message.answer(
            text=text,
            reply_markup=keyboard
        )

        return
    
    text, keyboard = await task_ser.save_new_task(company_id=company_id, user=user,
                                                  title=title, description=description,
                                                  db=db)
    
    await state.set_state(None)
    
    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )

# endregion