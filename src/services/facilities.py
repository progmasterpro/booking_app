from src.tasks.tasks import test_task
from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def facilities_get_all(self):
        return await self.db.facilities.get_all()

    async def facilities_add(self, facilities_data: FacilitiesAdd):
        facilities = await self.db.facilities.add(facilities_data)
        await self.db.commit()

        test_task.delay()
        return facilities