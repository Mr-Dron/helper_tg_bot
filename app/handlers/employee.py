from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

from app.models import Users, CompanyInvite
from app.services import employee as employee_ser
from app.repositories import employee as employee_rep
from app.keyboards import employee as employee_key

router = Router()

# region Меню всех сотрудников компании

@router.callback_query(F.data == "company_employees")
async def get_employees_company(callback: CallbackQuery,
                                state: FSMContext,
                                user: Users,
                                db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")

    text, keyboard = await employee_ser.employees_company_menu(current_page=1,
                                                         company_id=company_id,
                                                         db=db)

    await state.update_data(employee_current_page=1)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()

@router.callback_query(F.data.in_(["page_employees_previous", "page_employees_next"]))
async def navigation_employees_menu(callback: CallbackQuery,
                                    state: FSMContext,
                                    db: AsyncSession):
    
    data = await state.get_data()
    current_page = data.get("employee_current_page")
    company_id = data.get("comapny_id")

    if "next" in callback.data:
        current_page += 1
    else: 
        current_page -= 1
    
    text, keyboard = await employee_ser.employees_company_menu(current_page=1,
                                                         company_id=company_id,
                                                         db=db)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()
# endregion

# region добавление новго сотрудника

@router.callback_query(F.data == "add_new_employee")
async def add_new_employee(callback: CallbackQuery,
                           state: FSMContext,
                           user: Users,
                           db: AsyncSession):
    data = await state.get_data()
    company_id = data.get("company_id")

    invite = CompanyInvite(company_id=company_id)
    db.add(invite)
    await db.flush()

    invite_link = await create_start_link(callback.bot, f"inv_{invite.token}", encode=True)

    text = (
        "*Пригласительная ссылка создана*\n\n"
        "Перешлите ее новому сотруднику. Она будет активна 24 часа\n\n"
        f"`{invite_link}`"
    )
    keyboard = employee_key.return_employee_keyboard()

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()

# endregion

# region Карточка сотрудника

@router.callback_query(F.data.startswith("login_employee_"))
async def employee_card(callback: CallbackQuery,
                        state: FSMContext,
                        user: Users,
                        db: AsyncSession):
    
    employee_id = int(callback.data.split("_")[-1])

    data = await state.get_data()
    company_id = data.get("company_id")

    text, keyboard = await employee_ser.build_emlpoyee_card_context(employee_id=employee_id,
                                                                    company_id=company_id,
                                                                    db=db)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    await callback.answer()



# endregion
