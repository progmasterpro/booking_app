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

class HotelNotFoundException(NameAppException):
    detail = "Отель не найдет"

class RoomGetNotFoundException(NameAppException):
    detail = "Номер не найдет"