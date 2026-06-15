from aiogram import Router

from .create import router as create_router
from .view import router as view_router

department_router = Router()

department_router.include_routers(
    create_router,
    view_router
)