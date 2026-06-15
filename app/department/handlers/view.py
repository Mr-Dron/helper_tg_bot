import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.models import Users
from app.department import services, states, schemas

router = Router()

@router.callback_query(F.data == "company_departments")
async def get_company_deps(callback: CallbackQuery,
                           state: FSMContext,
                           user: Users,
                           db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")

    text, keyboard = await services.total_deps_menu(current_page=1,
                                                    company_id=company_id,
                                                    db=db)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

    await state.update_data(current_page=1)

@router.callback_query(F.data.in_(["previous_page_all_deps",
                                   "next_page_all_deps"]))
async def navigation_deps_menu(callback: CallbackQuery,
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
    
    text, keyboard = await services.total_deps_menu(current_page=current_page,
                                                    company_id=company_id,
                                                    db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

    await state.update_data(current_page=current_page)

@router.callback_query(F.data.startswith("login_dep_"))
async def current_dep_menu(callback: CallbackQuery,
                           state: FSMContext,
                           user: Users,
                           db: AsyncSession):
    
    data = await state.get_data()
    dep_id = data.get("dep_id")

    if not dep_id:
        dep_id = int(callback.data.split("_")[-1])

    text, keyboard = await services.login_dep(dep_id=dep_id,
                                              db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

    await state.update_data(current_page=None)

