import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import TaskStatus
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

    await state.update_data(task_id=None)
    data = await state.get_data()
    company_id = data.get("company_id")

    text, keyboard = await task_ser.build_task_menu_context(
        company_id=company_id,
        current_page=1,
        db=db
    )

    await state.update_data(current_page=1)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()

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

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()

# endregion

# region создание задач

@router.callback_query(F.data == "create_task")
async def create_task(callback: CallbackQuery,
                      state: FSMContext):
    
    await state.set_state(task_state.CreateTaskState.new_task)

    text, keyboard = await task_ser.build_task_create_context()

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

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

    promt_message = await callback.message.edit_text(
        text=text
    )

    await state.update_data(promt_msg_id=promt_message.message_id)
    
    await callback.answer()

@router.message(
    task_state.CreateTaskState.read_title
)
async def read_title(message: Message,
                     state: FSMContext):
    
    await state.update_data(title=message.text)
    await state.set_state(task_state.CreateTaskState.new_task)

    data = await state.get_data()
    description = data.get("description")
    promt_msg_id = data.get("promt_msg_id")

    if promt_msg_id:
        try: 
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=promt_msg_id
            )
        except:
            pass
    
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    except:
        pass

    asyncio.sleep(0.5)

    text, keyboard = await task_ser.build_task_create_context(title=message.text,
                                                              description=description)

    await message.answer(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
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
    promt_msg_id = data.get("promt_msg_id")

    if promt_msg_id:
        try: 
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=promt_msg_id
            )
        except:
            pass
    
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    except:
        pass

    asyncio.sleep(0.5)

    text, keyboard = await task_ser.build_task_create_context(description=message.text,
                                                              title=title)

    await message.answer(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
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
        await callback.message.edit_text(text="Заполните поля")
        text, keyboard = await task_ser.build_task_create_context(description=description,
                                                                  title=title)

        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
        await callback.answer()

        return
    
    text, keyboard = await task_ser.save_new_task(company_id=company_id, user=user,
                                                  title=title, description=description,
                                                  db=db)
    
    await state.set_state(None)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

# endregion

# region просмотр задач

@router.callback_query(F.data.startswith("login_task_"))
async def get_current_task(callback: CallbackQuery,
                           state: FSMContext,
                           user: Users,
                           db: AsyncSession):
    task_id = int(callback.data.split("_")[-1])

    await state.update_data(task_id=task_id)

    text, keyboard = await task_ser.current_task_menu(task_id=task_id,
                                                      db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

# endregion

# region редактирование задачи

@router.callback_query(F.data == "task_new_status")
async def edit_status_task(callback: CallbackQuery,
                           state: FSMContext,
                           user: Users,
                           db: AsyncSession):
    
    data = await state.get_data()
    task_id = data.get("task_id")

    text, keyboard = await task_ser.edit_status_task(task_id=task_id,
                                                     db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()

@router.callback_query(F.data.in_([status.name for status in TaskStatus]))
async def update_status(callback: CallbackQuery,
                        state: FSMContext,
                        db: AsyncSession):
    
    data = await state.get_data()
    task_id = data.get("task_id")

    await task_ser.uppend_status_task(task_id=task_id,
                                      new_status=callback.data,
                                      db=db)
    promt_message = await callback.message.edit_text(
        text="Статус задачи изменен"
    )

    text, keyboard = await task_ser.current_task_menu(task_id=task_id,
                                                      db=db)
    
    await promt_message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

@router.callback_query(F.data == "task_new_responsible")
async def choose_new_responsible(callback: CallbackQuery,
                                  state: FSMContext,
                                  user: Users,
                                  db: AsyncSession):
    data = await state.get_data()
    task_id = data.get("task_id")
    company_id = data.get("company_id")
    await state.update_data(choose_resp_current_page=1)

    text, keyboard = await task_ser.choose_new_responsible(current_page=1,
                                                           task_id=task_id,
                                                           company_id=company_id,
                                                           db=db)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

@router.callback_query(F.data.in_(["previuos_page_new_responsible",
                                   "next_page_new_responsible"]))
async def navigation_choose_new_resp(callback: CallbackQuery,
                                     state: FSMContext,
                                     user: Users,
                                     db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")
    task_id = data.get("task_id")
    current_page = data.get("choose_resp_current_page")

    if state.data.startswith("previous"):
        current_page -= 1
    else:
        current_page += 1

    text, keyboard = await task_ser.choose_new_responsible(current_page=current_page,
                                                           task_id=task_id,
                                                           company_id=company_id,
                                                           db=db)

    await state.update_data(choose_resp_current_page=current_page)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("new_responsible_"))
async def appoint_new_resp(callback: CallbackQuery,
                           state: FSMContext,
                           user: Users,
                           db: AsyncSession):
    
    resp_id = int(callback.data.split("_")[-1])
    
    data = await state.get_data()
    task_id = data.get("task_id")

    task = await task_rep.get_current_task(task_id=task_id,
                                           db=db)
    
    task.responsible_id = resp_id

    await db.commit()
    await db.refresh(task)

    text, keyboard = await task_ser.current_task_menu(task_id=task_id,
                                                      db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


# endregion
