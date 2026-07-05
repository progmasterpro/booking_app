from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.exeptions import ObjectNotFoundException, RoomNotFoundHTTPException, HotelNotFoundHTTPException, \
    RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, RoomPatch
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2026-03-11"),
        date_to: date = Query(example="2026-03-15"),
):
        return await RoomsService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить один номер")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
       return await RoomsService(db).get_one_with_rels(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

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
    try:
        room = await RoomsService(db).create_rooms(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полностью изменить данные номера")
async def edit_rooms(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    try:
        room = await RoomsService(db).edit_rooms(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK", "data": room}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично изменить данные номера")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    await RoomsService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def room_delete(hotel_id: int, room_id: int, db: DBDep):
    await RoomsService(db).room_delete(hotel_id, room_id)
    return {"status": "OK"}
