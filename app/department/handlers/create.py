import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.models import Users
from app.department import services, states, schemas

router = Router()

@router.callback_query(F.data == "create_dep")
async def create_department_menu(callback: CallbackQuery,
                                 state: FSMContext,
                                 db: AsyncSession,
                                 user: Users):

    fields = {
        "<b>Название</b>": None,
        "<b>Ответственный</b>": None,
        "<b>Создатель</b>": user.first_name,
    }

    text, keyboard = await services.create_dep_menu(fields=fields)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

@router.callback_query(F.data == "edit_name_new_dep")
async def write_new_name(callback: CallbackQuery,
                         state: FSMContext,
                         user: Users,
                         db: AsyncSession):
    
    await state.set_state(states.CreateDepartment.edit_name)

    promt_message = await callback.message.edit_text(
        text="Введите название отдела",
        parse_mode=ParseMode.HTML
    )

    await state.update_data(promt_msg_id=promt_message.message_id)

@router.message(states.CreateDepartment.edit_name)
async def read_new_name(message: Message,
                        state: FSMContext,
                        user: Users,
                        db: AsyncSession):
    
    name = message.text
    await state.update_data(name=name)

    data = await state.get_data()
    company_id = data.get("company_id")
    resp_id = data.get("resp_id")
    promt_msg_id = data.get("promt_msg_id")


    try:
        await message.bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=[promt_msg_id, message.message_id]
        )
        asyncio.sleep(0.5)
    except:
        pass

    fields = {
        "<b>Название</b>": name,
        "<b>Ответственный</b>": resp_id,
        "<b>Создатель</b>": user.first_name,
    }

    text, keyboard = await services.create_dep_menu(fields=fields,
                                                    name=name)
    
    await message.answer(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await state.set_state(None)
    await state.update_data(promt_msg_id=None)


@router.callback_query(F.data == "new_resp_new_dep")
async def edit_resp_menu(callback: CallbackQuery,
                         state: FSMContext,
                         user: Users,
                         db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")

    text, keyboard = await services.select_resp_from_employees(current_page=1,
                                                               company_id=company_id,
                                                               db=db)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

    await state.update_data(current_page=1)
    

@router.callback_query(F.data.in_(["previous_page_resp_new_dep",
                                   "next_page_resp_new_dep"]))
async def navigation_edit_resp_menu(callback: CallbackQuery,
                                    state: FSMContext,
                                    user: Users,
                                    db: AsyncSession):
    data = await state.get_data()
    company_id = data.get("company_id")
    current_page = data.get("current_page")

    if callback.data.startswith("previous"):
        current_page -= 1
    else:
        current_page += 1
    
    text, keyboard = await services.select_resp_from_employees(current_page=current_page,
                                                               company_id=company_id,
                                                               db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

@router.callback_query(F.data.startswith("select_new_resp_"))
async def save_new_resp(callback: CallbackQuery,
                        state: FSMContext,
                        user: Users,
                        db: AsyncSession):
    
    resp_id = int(callback.data.split("_")[-1])

    data = await state.get_data()
    company_id = data.get("company_id")
    name = data.get("name")

    await state.update_data(resp_id=resp_id)

    fields = {
        "<b>Название</b>": name,
        "<b>Ответственный</b>": resp_id,
        "<b>Создатель</b>": user.first_name,
    }

    text, keyboard = await services.create_dep_menu(fields=fields,
                                                    name=name)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    
    await callback.answer()

    await state.update_data(current_page=None)

@router.callback_query(F.data.in_(["inactive_save_new_dep",
                                   "active_save_new_dep"]))
async def save_new_dep(callback: CallbackQuery,
                       state: FSMContext,
                       user: Users,
                       db: AsyncSession):
    
    if callback.data.startswith("inactive"):
        await callback.message.edit_text(
            text="<strong>Заполните данные</strong>",
            parse_mode=ParseMode.HTML
        )

        data = await state.get_data()
        resp_id = data.get("resp_id")
        name = data.get("name")

        await state.update_data(resp_id=resp_id)

        fields = {
            "<b>Название</b>": name,
            "<b>Ответственный</b>": resp_id,
            "<b>Создатель</b>": user.first_name,
        }

        text, keyboard = await services.create_dep_menu(fields=fields,
                                                        name=name)

        asyncio.sleep(0.5)

        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

        await callback.answer()

        return



    data = await state.get_data()
    comapny_id = data.get("company_id")
    name = data.get("name")
    resp_id = data.get("resp_id")

    data = schemas.DepartmentCreate(
        name=name,
        responsible_id=resp_id,
        creator=user,
        company_id=comapny_id
    )

    text, keyboard, dep_id = await services.save_new_dep(data=data, db=db)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

    await state.update_data(resp_id=None, 
                            name=None,
                            dep_id=dep_id)


