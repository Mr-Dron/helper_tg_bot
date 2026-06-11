from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user as user_rep
from app.helpers import profile as profile_help
from app.models import Users
from app.keyboards import profile as profile_key, menu


async def send_profile_menu(user: Users):

    text = await profile_help.build_profile_text(user)

    keyboard = menu.back_menu()

    return text, keyboard

async def send_update_profile_menu(user: Users):

    text = await profile_help.build_profile_text(user)

    keyboard = profile_key.update_menu()

    return text, keyboard