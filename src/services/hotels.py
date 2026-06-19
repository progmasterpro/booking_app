from datetime import date

from src.exeptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, Hotel
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            title: str,
            location: str,
            date_from: date,
            date_to: date,
    ):
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

    async def hotel_get_one(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def hotels_add(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def hotels_edit(self, data: HotelAdd, hotel_id: int):
        hotel = await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()
        return hotel

    async def hotels_edit_part(self, data: HotelAdd, hotel_id: int):
        hotel = await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return hotel

    async def hotel_delete (self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_exist_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException