import asyncio
from aiogram import Bot, Dispatcher

from app.core.settings import settings
from app.handlers.main import router
from app.middleware.context import DBUserMiddleware

async def main():

    bot = Bot(token=settings.BOT_TOKEN)
    
    db = Dispatcher()
    db.include_router(router)

    db.update.middleware(DBUserMiddleware())

    await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())