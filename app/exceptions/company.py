from app.exceptions.common import NotFoundError

class CompaniesNotFoundError(NotFoundError):
    def __init():
        super().__init__(f"Компании не найдены")