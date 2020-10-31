from pydantic import BaseModel

class RoomSchema(BaseModel):
    type: str
    owner: str
    owner_id: int
    price_per_day: float

class RoomDB(RoomSchema):
	id: int