from aiogram import BaseMiddleware
from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import Users


class DBUserMiddleware(BaseMiddleware):

    async def __call__(self, 
                       handler: Callable, 
                       event, 
                       data: dict[str, Any]
                       ):
        
        async with AsyncSessionLocal() as session:
            try:
                data["db"] = session

                telegram_user = data.get("event_from_user")

                user = (await session.execute(select(Users).
                                                where(Users.telegram_id == telegram_user.id))
                                                ).scalar_one_or_none()
                
                if not user:
                    user = Users(
                        telegram_id= telegram_user.id,
                        telegram_url=f"https://t.me/{telegram_user.username}",
                        username=telegram_user.username,
                        first_name=telegram_user.first_name
                    )

                    session.add(user)

                    await session.flush()
                
                data["user"] = user

                response = await handler(event, data)

                await session.commit()

                return response
            
            except:
                await session.rollback()
                raise

            finally:
                await session.close()
        