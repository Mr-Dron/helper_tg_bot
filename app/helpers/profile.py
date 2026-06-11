from app.models import Users

async def build_profile_text(user: Users):
    return (
        f"Имя: {user.first_name}\n"
        f"Имя пользователя: {user.username}\n"
        f"Ссылка: {user.telegram_url}"
    )