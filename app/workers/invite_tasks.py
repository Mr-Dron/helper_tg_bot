import asyncio
from datetime import datetime, timezone
from sqlalchemy import delete

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models import CompanyInvite

@celery_app.task
def clear_expired_invites_task():
    return asyncio.run(_db_clear_invites())

async def _db_clear_invites():
    async with AsyncSessionLocal() as session:
        query = delete(CompanyInvite).where(CompanyInvite.expires_at <= datetime.now(timezone.utc))
        result = await session.execute(query)
        await session.commit()
        return f"Удалено устаревших инвайтов {result.rowcount}"