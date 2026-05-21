from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends

from app.dependencies.db import get_session
from app.models import Users
from app.exceptions import user as user_exc

async def get_current_user(
        telegram_id: int,
        db: AsyncSession = Depends(get_session)
):
    user = (await db.execute(
        select(Users).where(Users.telegram_id == telegram_id)
    )).scalar_one_or_none()

    if not user:
        raise user_exc.UserNotFoundError()
    
    return user