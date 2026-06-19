from datetime import date

from src.api.dependencies import DBDep
from src.exeptions import HotelNotFoundHTTPException, HotelNotFoundException, ObjectNotFoundException, \
    RoomNotFoundException
from src.schemas.facilities import RoomFacilitiesAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.services.base import BaseService
from src.services.hotels import HotelsService


class RoomsService(BaseService):
    # Получить все номера
    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if not hotel:
            raise HotelNotFoundException
        return await self.db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    # Получить один номер
    async def get_one_with_rels(
            self,
            hotel_id: int,
            room_id: int):
        await HotelsService(self.db).get_hotel_exist_check(hotel_id)
        return await self.db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)

    # Добавить номер
    async def create_rooms(
            self,
            hotel_id: int,
            room_data: RoomAddRequest,
    ):
        await HotelsService(self.db).get_hotel_exist_check(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        room_facilities_data = [
            RoomFacilitiesAdd(room_id=room.id, facilities_id=f_id) for f_id in room_data.facilities_ids
        ]
        # room_id, facilities_id это атрибуты схемы RoomFacilitiesAdd
        # room.id берется из room = await db.rooms.add(_room_data), который возвращает схему Room, в которой есть id
        # room_data  - это схема - RoomAddRequest, в ней есть параметр facilities_ids
        await self.db.rooms_facilities.add_bulk(room_facilities_data)
        await self.db.commit()

    # Полностью изменить данные номера
    async def edit_rooms(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomAddRequest,
    ):
        await HotelsService(self.db).get_hotel_exist_check(hotel_id)
        await self.get_room_exist_check(room_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
        await self.db.commit()

    # частично изменить данные номера
    async def partially_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest,
    ):
        await HotelsService(self.db).get_hotel_exist_check(hotel_id)
        await self.get_room_exist_check(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
        await self.db.session.commit()

    # удалить номер
    async def room_delete(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).get_hotel_exist_check(hotel_id)
        await self.get_room_exist_check(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_exist_check(self, room_id):
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException