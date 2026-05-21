from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users
from app.schemas import user as user_sch

async def create_user_req(data: user_sch.UserCreate, db: AsyncSession):
    
    new_user = Users(**data)

    db.add(new_user)
    
    await db.commit()
    await db.refresh(new_user)

    return new_user