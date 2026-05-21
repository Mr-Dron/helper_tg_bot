from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user as user_rep
from app.schemas import user as user_sch

async def create_user(data: user_sch.UserCreate, db: AsyncSession):
    return await user_rep.create_user_req(data, db)

# async def out_data_current_user(user: User):
#     ...