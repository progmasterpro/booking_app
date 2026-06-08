from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=15)
async def facilities_get(db: DBDep):
    print("go to DB")
    return await db.facilities.get_all()



@router.post("", summary="Добавление удобств общая")
async def facilities_add(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "data": facilities}

# @router.post("", summary="Добавление удобства для конкретного номера")
# async def facilities_add_room(facilities_data_room: )
      # """
      # INSERT INTO Books
      # VALUES(6, 'Animal Farm', 'George Orwell', NULL);
      # """

