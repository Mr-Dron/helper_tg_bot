from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import Tasks

async def get_tasks_company(company_id: int, page: int, db: AsyncSession) -> list[Tasks]:

    stmt = (
        select(Tasks)
        .where(Tasks.company_id == company_id)
        .limit(4)
        .offset((page-1)*4)
    )

    tasks = (await db.execute(stmt)).scalars().all()

    if not tasks:
        return []

    return tasks

async def get_count_tasks_company(company_id: int, db: AsyncSession):

    stmt = (
        select(func.count(Tasks.id))
        .where(Tasks.company_id == company_id)
    )

    count_tasks = (await db.execute(stmt)).scalar()

    return count_tasks