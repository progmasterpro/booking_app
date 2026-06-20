from fastapi import HTTPException


class NameAppException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class NameAppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code = self.status_code, detail = self.detail)


class ObjectNotFoundException(NameAppException):
    detail = "Объект не найден"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class ObjectAlreadyExistException(NameAppException):
    detail = "Похожий объект уже существует"

class AllRoomBookedException(NameAppException):
    detail = "Закончились номера для бронирования"

class AllRoomBookedHTTPException(NameAppHTTPException):
    status_code = 409
    detail = "Закончились номера для бронирования"

class HotelNotFoundHTTPException(NameAppHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(NameAppHTTPException):
    status_code = 404
    detail = "Номер не найден"


class DateFromGtDateTo(NameAppException):
    detail = "Дата заезда позже, чем дата выезда"

class DateFromGtDateToHTTPException(NameAppHTTPException):
    status_code = 422
    detail = "Дата заезда позже, чем дата выезда"




