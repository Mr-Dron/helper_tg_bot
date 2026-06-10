from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, and_, join, outerjoin

from app.models import EmployeesCompany, CompanyInvite, Users, Tasks

async def get_employee_company(current_page: int, company_id: int, db: AsyncSession):

    stmt = (
        select(EmployeesCompany)
        .where(EmployeesCompany.company_id == company_id)
        .options(joinedload(EmployeesCompany.employees))
        .limit(4)
        .offset((current_page - 1) * 4)
    )

    employees = (await db.execute(stmt)).scalars().all()

    return employees

async def get_count_employees_company(company_id: int, db: AsyncSession):

    stmt = (
        select(func.count(EmployeesCompany.id))
        .where(EmployeesCompany.company_id == company_id)
    )

    count_emp = (await db.execute(stmt)).scalar()

    return count_emp

async def check_invite_token(token: str, db: AsyncSession):

    stmt = (
        select(CompanyInvite)
        .where(CompanyInvite.token == token)
    )

    invite = (await db.execute(stmt)).scalar_one_or_none()

    return invite

async def check_exists_employee(company_id: int, telegram_id: int, db: AsyncSession):

    stmt = (
        select(EmployeesCompany)
        .join(Users, Users.telegram_id == telegram_id)
        .where(and_(EmployeesCompany.company_id == company_id,
                    EmployeesCompany.user_id == Users.id))
    )

    user = (await db.execute(stmt)).scalar_one_or_none()

    return user

async def add_new_employee(comapny_id: int, telegram_id: int, db: AsyncSession):

    user = (await db.execute(
        select(Users)
        .where(Users.telegram_id == telegram_id)
    )).scalar_one_or_none()

    new_employee = EmployeesCompany(company_id=comapny_id,
                                    user_id = user.id)
    
    db.add(new_employee)
    await db.flush()

async def get_employees_company_with_tasks(current_page: int, company_id: int,
                                           db: AsyncSession):
    
    stmt = (
        select(
            EmployeesCompany,
            Users,
            func.count(Tasks.id).label("tasks_count")
        )
        .join(EmployeesCompany.employees)
        .outerjoin(Users.assigned_tasks)
        .where(EmployeesCompany.company_id == company_id)
        .group_by(EmployeesCompany.id, Users.id)
        .limit(4)
        .offset((current_page - 1) * 4)
    )

    employees = (await db.execute(stmt)).all()

    return employees