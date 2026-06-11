from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import employee as employee_rep
from app.keyboards import employee as employee_key
from app.helpers import employee as employee_help

async def employees_company_menu(current_page: int, 
                                 company_id: int, db: AsyncSession):

    employees = await employee_rep.get_employee_company(current_page=current_page,
                                                        company_id=company_id,
                                                        db=db)
    
    total_page = await employee_help.count_total_pages(company_id=company_id,
                                                 db=db)

    keyboard = employee_key.employees_menu_keyboard(employees_list=employees,
                                                    total_page=total_page,
                                                    current_page=current_page)

    text = await employee_help.employees_company_menu_text(current_page=current_page,
                                                           total_page=total_page,
                                                           employees_list=employees)

    return text, keyboard

async def build_emlpoyee_card_context(employee_id: int, company_id: int, 
                                      db: AsyncSession):
    
    employee = await employee_rep.get_current_employee_company(company_id=company_id,
                                                               employee_id=employee_id,
                                                               db=db)
    keyboard = employee_key.employee_card_keyboard(employee_id=employee_id)
    
    text = await employee_help.employee_card_menu_text(employee=employee)

    return text, keyboard