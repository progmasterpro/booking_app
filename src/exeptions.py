from fastapi import HTTPException


class NameAppException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NameAppException):
    detail = "Объект не найдет"

class ObjectAlreadyExistException(NameAppException):
    detail = "Похожий объект уже существует"

class AllRoomBookedException(NameAppException):
    detail = "Закончились номера для бронирования"

class DateFromGtDateTo(NameAppException):
    detail = "Дата заезда позже, чем дата выезда"

class NameAppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code = self.status_code, detail = self.detail)

class HotelNotFoundHTTPException(NameAppHTTPException):
    status_code = 404
    detail = "Отель не найдет"

class RoomNotFoundHTTPException(NameAppHTTPException):
    status_code = 404
    detail = "Номер не найдет"


