from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.exeptions import AllRoomBookedException,AllRoomBookedHTTPException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("", summary="Получение всех бронирований")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()

@router.get("/me", summary="Получение бронирования текущего пользователя")
async def get_me_booking(user_id: UserIdDep, db: DBDep):
    return await BookingsService(db).get_me_booking(user_id)


@router.post("", summary="Добавление бронирования")
async def bookings_add(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingsService(db).bookings_add(user_id, booking_data)
    except AllRoomBookedException:
        raise AllRoomBookedHTTPException
    return {"status": "ok", "data": booking}
