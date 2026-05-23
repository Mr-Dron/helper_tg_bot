from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user as user_rep
from app.schemas import user as user_sch
from app.models import Users
from app.keyboards import profile

async def build_profile_text(user: Users):
    return (
        f"Имя: {user.first_name}\n"
        f"Имя пользователя: {user.username}\n"
        f"Ссылка: {user.telegram_url}"
    )

async def send_update_profile_menu(target, user: Users):

    text = await build_profile_text(user)

    await target.answer(
        text,
        reply_markup=profile.update_menu()
    )