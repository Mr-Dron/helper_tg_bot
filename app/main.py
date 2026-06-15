import asyncio
from redis.asyncio import Redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage


from app.core.settings import settings
from app.handlers import ROUTERS
from app.department import department_router
from app.middleware.context import DBUserMiddleware

async def main():

    redis_client = Redis(host=settings.REDIS_HOST,
                         port=settings.REDIS_PORT,
                         decode_responses=True)
    
    storage = RedisStorage(redis=redis_client)

    bot = Bot(token=settings.BOT_TOKEN)
    
    ROUTERS.append(department_router)

    db = Dispatcher(storage=storage)
    db.include_routers(*ROUTERS)

    db.update.middleware(DBUserMiddleware())

    await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())