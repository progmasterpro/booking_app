from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str


class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facilities_id: int

class RoomFacilities(RoomFacilitiesAdd):
    id: int