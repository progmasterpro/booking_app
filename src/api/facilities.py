from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=15)
async def facilities_get(db: DBDep):
    return await FacilityService(db).facilities_get_all()


@router.post("", summary="Добавление удобств общая")
async def facilities_add(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facilities = await FacilityService(db).facilities_add(facilities_data)
    return {"status": "ok", "data": facilities}