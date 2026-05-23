import asyncio
from aiogram import Bot, Dispatcher

from app.core.settings import settings
from app.handlers import router_main, router_prof
from app.middleware.context import DBUserMiddleware

async def main():

    bot = Bot(token=settings.BOT_TOKEN)
    
    db = Dispatcher()
    db.include_routers(router_prof, router_main)

    db.update.middleware(DBUserMiddleware())

    await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())