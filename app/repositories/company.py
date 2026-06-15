from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import Users, Companies, EmployeesCompany, Tasks

async def get_companies_req(user: Users, db: AsyncSession):
    
    stmt = (
        select(Companies)
        .join(Companies.employees)
        .where(EmployeesCompany.user_id == user.id)
    )

    companies = (await db.execute(stmt)).scalars().all()

    if not companies:
        return []
    
    return companies

# общаяя
async def get_company_by_id_req(company_id: int, db: AsyncSession):

    stmt = (
        select(Companies)
        .where(Companies.id == company_id)
    )

    company = (await db.execute(stmt)).scalar_one_or_none()

    return company

async def get_company_for_preview(company_id: int, db: AsyncSession):

    employees_subq = (
        select(func.count(EmployeesCompany.user_id))
        .where(EmployeesCompany.company_id == company_id)
        .correlate(Companies)
        .scalar_subquery()
    )

    tasks_subq = (
        select(func.count(Tasks.id))
        .where(Tasks.company_id == company_id)
        .correlate(Companies)
        .scalar_subquery()
    )

    stmt = (
        select(Companies, employees_subq.label("employees_subq"), tasks_subq.label("tasks_subq"))
        .where(Companies.id == company_id)
    )

    result = (await db.execute(stmt)).one_or_none()

    if not result:
        return None

    return result