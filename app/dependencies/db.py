from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()