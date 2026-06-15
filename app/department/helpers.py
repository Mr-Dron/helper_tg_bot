import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EmployeesCompany, Departments
from app.repositories import employee as employe_rep

async def text_create_department_menu(fields: dict):

    lines = [
        f"{label}: {value}" if value else "<i>Не заполнено</i>"
        for label, value in fields.items()
    ]

    return "<b>Новый отдел</b>\n\n" + "\n".join(lines)

async def count_page_employees(company_id: int, db: AsyncSession):

    count_employees = await employe_rep.get_count_employees_company(company_id=company_id,
                                                                 db=db)
    
    total_page = math.ceil(count_employees / 4)
    if total_page == 0:
        total_page += 1

    return total_page

async def select_new_resp(employees: list[EmployeesCompany], current_page: int, 
                          total_page: int):
    
    lines = [
        f"<b>#{employee.employees.id}</b>: {employee.employees.first_name} <i>Должность (в разработке)</i>"
        for employee in employees
    ]

    return "<strong>Выберите ответственного</strong>\n\n" + "\n".join(lines) + f"\nСтраница {current_page} из {total_page}"

async def text_card_dep(data_dep: Departments, mode: str = "view"):

    fields = {
        "Название отдела": data_dep.name,
        "Ответсвенный": data_dep.responsible.first_name,
        "Создатель": data_dep.creator.first_name,
        "Компания": data_dep.company.name
    }

    lines = [
        f"{label}: {value if value else '<i>Не заполнено</i>'}"
        for label, value in fields.items()
    ]

    if mode == "create":
        return "<strong>Новый отдел создан</strong>\n\n" + "\n".join(lines)
    
    return "<strong>Карточка отдела</strong>\n\n" + "\n".join(lines)


async def total_page_deps(total_count: int):

    total_page = math.ceil(total_count / 4)

    if total_page == 0:
        total_page += 1
    
    return total_page

async def all_deps_menu(current_page: int, total_page: int, deps: Departments):

    lines = [
        f"Отдел <u>#{dep.id}</u>: {dep.name}"
        for dep in deps
    ]

    return f"<strong>Список отделов компании</strong>\n\n" + "\n".join(lines) + f"\n\n<i>Страница {current_page} из {total_page} </i>"
