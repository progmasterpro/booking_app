from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.exeptions import RoomsDateFromGtDateTo, RoomGetNotFoundException, HotelNotFoundException
from src.repositories.rooms import RoomsRepositories
from src.schemas.facilities import RoomFacilitiesAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2026-03-11"),
        date_to: date = Query(example="2026-03-15"),
):
    try:
        return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    except RoomsDateFromGtDateTo as e:
        raise HTTPException(status_code=422, detail=e.detail)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить один номер")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавить номер")
async def create_rooms(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples={
    "1": Example(
        summary="Rooms lux",
        value={
            "title": "lux rooms forever",
            "description": "Супер дорогой люкс",
            "price": 2000,
            "quantity": 10,
            "facilities_ids": [1, 2, 3],
        },
    ),
    "2": Example(
        summary="Rooms middle",
        value={
            "title": "lux rooms middle",
            "description": "Номер средней категории",
            "price": 1000,
            "quantity": 20,
            "facilities_ids": [1, 2, 3],
        }
    )
}
        )
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    room_facilities_data = [RoomFacilitiesAdd(room_id=room.id, facilities_id=f_id) for f_id in room_data.facilities_ids]
    # room_id, facilities_id это атрибуты схемы RoomFacilitiesAdd
    # room.id берется из room = await db.rooms.add(_room_data), который возвращает схему Room, в которой есть id
    # room_data  - это схема - RoomAddRequest, в ней есть параметр facilities_ids
    await db.rooms_facilities.add_bulk(room_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полностью изменить данные номера")
async def edit_rooms(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично изменить данные номера")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def room_delete(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepositories(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
