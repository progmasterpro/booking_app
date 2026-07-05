from src.api.dependencies import UserIdDep
from src.exeptions import AllRoomBookedException, ObjectNotFoundException, RoomNotFoundException, HotelNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingsService(BaseService):
    # Получение всех бронирований
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    # Получение бронирования текущего пользователя
    async def get_me_booking(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    # Добавление бронирования
    async def bookings_add(
            self,
            user_id: UserIdDep,
            booking_data: BookingAddRequest,
    ):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

