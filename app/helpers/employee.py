import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EmployeesCompany
from app.repositories import employee as employee_rep

async def employees_company_menu_text(current_page: int, total_page: int,
                                      employees_list: list[EmployeesCompany]):
    
    text = ""

    for employee in employees_list:
        text += f"#{employee.user_id} {employee.employees.first_name} (_должность_)\n"
    
    text += f"\nСтраница {current_page} из {total_page}"

    return text

async def count_total_pages(company_id: int, db: AsyncSession):

    count_employees = await employee_rep.get_count_employees_company(company_id=company_id,
                                                                     db=db)
    
    total_page = math.ceil(count_employees / 4)

    if total_page == 0:
        total_page = 1

    return total_page
