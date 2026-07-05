from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi.openapi.models import Example

from src.api.dependencies import PaginationDep, DBDep
from src.exeptions import HotelNotFoundHTTPException, ObjectNotFoundException, \
    DateFromGtDateToHTTPException, NameAppHTTPException, DateFromGtDateTo
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelsService

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("", summary="Получить все отели")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
        date_from: date = Query(example="2026-03-11", description="Дата заезда"),
        date_to: date = Query(example="2026-03-15", description="Дата выезда"),
):
    try:
        hotel = await HotelsService(db).get_filtered_by_time(
            pagination,
            title,
            location,
            date_from,
            date_to,
        )
        return {"status": "OK", "data": hotel}
    except DateFromGtDateTo:
        raise DateFromGtDateToHTTPException

@router.get("/{hotel_id}", summary="Получить отель по id")
async def get_hotel_id(hotel_id: int, db: DBDep):
    try:
        return await HotelsService(db).hotel_get_one(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

@router.post("", summary="Добавить отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
        "1": Example (
            summary= "Moscow",
            value = {
                "title": "Dvorec 5 stars",
                "location": "ул. Колесова, д. 5, г. Москва"
                    }
    ),
        "2": Example (
            summary="Piter",
            value= {
                "title": "Piter life",
                "location": "ул. Речная, д. 14, г. Санкт-Петербург"
                    }
                )
            }
        )
):
    hotel = await HotelsService(db).hotels_add(hotel_data)
    return {"status": "OK", "data": hotel}
        # hotel.compile(engine, compile_kwargs={"literal_binds": True})


@router.put("/{hotel_id}", summary="Обновление всех данных об отеле (title, location)")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep,
):
    hotel = await HotelsService(db).hotels_edit(hotel_data, hotel_id)
    return {"status": "OK", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле, (title или location)",
    description="<h1>Тут мы частично обновляем данные об отеле: можно обновить location, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):
    hotel = await HotelsService(db).hotels_edit_part(hotel_data, hotel_id)
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelsService(db).hotel_delete(hotel_id)
    return {"status": "OK"}
