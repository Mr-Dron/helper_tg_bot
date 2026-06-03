from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup

from app.keyboards import company as company_key
from app.models import Companies, Users, EmployeesCompany
from app.helpers import company as company_help

async def create_company(name: str, user: Users, db: AsyncSession) -> Companies:

    new_company_data = {
        "name": name,
        "creator_id": user.id,
    }

    new_company = Companies(**new_company_data)

    db.add(new_company)

    await db.flush()

    await add_new_employe(user, new_company, db)

    return new_company

async def add_new_employe(user: Users, company: Companies, db: AsyncSession):

    if company_help.employe_exists(user, company, db):

        new_employe = EmployeesCompany(
            company_id = company.id,
            user_id = user.id
        )

        db.add(new_employe)

        await db.flush()
    
    return 