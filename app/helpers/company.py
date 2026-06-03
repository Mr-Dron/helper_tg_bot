from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Users, Companies, EmployeesCompany

async def employe_exists(user: Users, company: Companies, db: AsyncSession):

    employe = (await db.execute(
        select(EmployeesCompany)
        .where(and_(
            EmployeesCompany.user_id == user.id,
            EmployeesCompany.company_id == company.id
        ))
    )).scalar_one_or_none()

    if not employe:
        return True
    
    return False
