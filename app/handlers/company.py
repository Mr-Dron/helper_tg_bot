from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users
from app.repositories import company as company_rep
from app.keyboards import company as company_key
from app.services import company as company_ser
from app.states import company as company_state

router = Router()

# region получение компаний
@router.callback_query(F.data == "my_companies")
async def get_my_companies(callback: CallbackQuery,
                           user: Users,
                           db: AsyncSession):
    
    companies = await company_rep.get_companies_req(user, db)
    keyboard = company_key.choice_company_menu(companies)

    if not companies:
        await callback.message.answer(
            text="Нет активный компаний",
            reply_markup=keyboard
        )
        return 

    await callback.message.answer(
        text="Список компаний",
        reply_markup=keyboard
    )
# endregion 

# region создание компаний

@router.callback_query(F.data == "create_company")
async def create_companies(callback: CallbackQuery,
                           state: FSMContext):
    await state.set_state(company_state.CreateProfileState.new_company)

    text = "Введите название компании:"

    await callback.message.answer(
        text=text,
        reply_markup=company_key.return_to_menu()
    )

@router.message(
    company_state.CreateProfileState.new_company
)
async def read_new_company_data(message: Message,
                                state: FSMContext,
                                user: Users,
                                db: AsyncSession):
    
    company = await company_ser.create_company(message.text, user, db)

    text = "Новая компания:\n"\
           f"ID - {company.id}\n"\
           f"Название - {company.name}\n"\
           f"Создатель - {company.creator_id}"

    await state.update_data(company_id=company.id)

    await message.answer(
        text,
        reply_markup=company_key.login_company_keyboard()
    )

# endregion 

# region меню компании

@router.callback_query(F.data.startswith("preview_company"))
async def preview_company(callback: CallbackQuery,
                          state: FSMContext,
                          user: Users,
                          db: AsyncSession
                          ):
    
    company_id = int(callback.data.split("_")[-1])
    company, employees_count, tasks_count = await company_rep.get_company_for_preview(company_id=company_id,
                                                                                           db=db)
    
    text = f"Название: {company.name}\n"\
           f"Сотрудники: {employees_count}\n"\
           f"Задачи: {tasks_count}"

    await state.update_data(company_id=company_id)

    await callback.message.answer(
        text=text,
        reply_markup=company_key.login_company_keyboard()
    )

@router.callback_query(F.data.in_({"login_company", "company_menu"}))
async def company_menu(callback: CallbackQuery,
                       state: FSMContext,
                       user: Users,
                       db: AsyncSession):
    
    data = await state.get_data()
    company_id = data.get("company_id")
    company = await company_rep.get_company_by_id_req(company_id=company_id,
                                                      db=db)

    text = f"Компания {company.name}:\n"\
           f"ID - {company.id}\n"\
           f"Создатель - {company.creator_id}"
    
    await callback.message.answer(
        text=text,
        reply_markup=company_key.company_menu_keyboard()
    )

# endregion

