class AppExceptions(Exception):
    def __init__(self,
                 detail: str,
                 status_code: int | None = None):
        self.detail = detail
        self.status_code = status_code

        super().__init__(detail)

class NotFoundError(AppExceptions):
    def __init__(self,
                 detail: str = "Сущность не найдена"):
        super().__init__(detail)