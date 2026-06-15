from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, and_, func

from app.models import Departments, DepartmentMembers
from app.department import schemas

async def create_dep(data: schemas.DepartmentCreate, db: AsyncSession):
    new_dep = Departments(
        name=data.name,
        responsible_id=data.responsible_id,
        creator_id=data.creator.id,
        company_id=data.company_id
    )

    db.add(new_dep)

    await db.commit()
    await db.refresh(new_dep)

    return new_dep

async def add_new_member(member_id: int, dep_id: int, db: AsyncSession):

    new_member_dep = DepartmentMembers(
        user_id = member_id,
        departmant_id = dep_id
    )

    db.add(new_member_dep)

    await db.commit()

async def check_to_exists_member(member_id: int, dep_id: int, db: AsyncSession):

    stmt = (
        select(DepartmentMembers)
        .where(and_(DepartmentMembers.user_id == member_id,
                    DepartmentMembers.departmant_id == dep_id))
    )

    member = (await db.execute(stmt)).scalar_one_or_none()

    return member

async def get_current_dep(dep_id: int, db: AsyncSession):

    stmt = (
        select(Departments)
        .options(joinedload(Departments.company),
                 joinedload(Departments.creator),
                 joinedload(Departments.responsible))
        .where(Departments.id == dep_id)
    )

    dep = (await db.execute(stmt)).scalar_one_or_none()

    return dep

async def get_company_deps(current_page: int, company_id: int, db: AsyncSession):

    stmt = (
        select(Departments)
        .where(Departments.company_id == company_id)
        .limit(4)
        .offset((current_page - 1) * 4)
    )

    deps = (await db.execute(stmt)).scalars().all()

    return deps

async def total_count_deps_company(company_id: int, db: AsyncSession):

    stmt = (
        select(func.count(Departments.id))
        .where(Departments.company_id == company_id)
    )

    total_count = (await db.execute(stmt)).scalar()

    return total_count

