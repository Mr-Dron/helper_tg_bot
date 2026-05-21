from app.exceptions.common import NotFoundError, AppExceptions

class UserNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(f"Пользователь не найдет")