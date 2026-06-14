from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi.openapi.models import Example

from src.api.dependencies import PaginationDep, DBDep
from src.exeptions import HotelDateFromGtDateTo, HotelNotFoundException
from src.schemas.hotels import HotelPatch, HotelAdd

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
    per_page = pagination.per_page or 5

    try:
        return await db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=per_page * (pagination.page-1)
        )
    except HotelDateFromGtDateTo as e:
        raise HTTPException(status_code=422, detail=e.detail)
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.get("/{hotel_id}", summary="Получить отель по id")
async def get_hotel_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}
        # hotel.compile(engine, compile_kwargs={"literal_binds": True})


@router.put("/{hotel_id}", summary="Обновление всех данных об отеле (title, location)")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле, (title или location)",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
