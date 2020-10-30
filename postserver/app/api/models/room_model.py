from pydantic import BaseModel

class RoomSchema(BaseModel):
    price_per_day: float
    accommodation_type: str

class RoomDB(RoomSchema):
	id: int