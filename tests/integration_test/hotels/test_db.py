from src.schemas.hotels import HotelAdd


async def test_hotel_add(db):
    hotel_data = HotelAdd(title="Hotel 1", location="Сочи")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()





