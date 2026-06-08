from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    data_booking = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=5, day=3),
        date_to=date(year=2026, month=5, day=7),
        price=100
    )
    new_booking = await db.bookings.add(data_booking)

    # получение бронирования
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # обновление бронирования
    date_to_update = date(year=2026, month=5, day=10)
    data_update_booking = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=5, day=3),
        date_to=date_to_update,
        price=100
    )
    await db.bookings.edit(data_update_booking, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id = new_booking.id)

    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == date_to_update

    # удаление бронирования
    await db.bookings.delete(id=new_booking.id)

    booking_after_del = await db.bookings.get_one_or_none(id = new_booking.id)
    assert not booking_after_del