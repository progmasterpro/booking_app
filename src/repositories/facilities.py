from sqlalchemy import select, delete, insert

from src.models.facilities import RoomsFacilitiesModel, FacilitiesModel
from src.repositories.base import BaseRepositories
from src.repositories.mappers.mappers import FacilitiesDataMapper
from src.schemas.facilities import RoomFacilities


class FacilitiesRepositories(BaseRepositories):
    model = FacilitiesModel
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepositories(BaseRepositories):
    model = RoomsFacilitiesModel
    schema = RoomFacilities

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = (
            select(self.model.facilities_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(query)
        current_facilities_ids: list[int] = res.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))  # [1, 2] - [2, 3]
        ids_to_insert = list(set(facilities_ids) - set(current_facilities_ids))  # [2, 3] - [1, 2]

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .where(
                    self.model.room_id==room_id,
                    self.model.facilities_id.in_(ids_to_delete))
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stm = (
                insert(self.model)
            .values([{"room_id": room_id, "facilities_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stm)
