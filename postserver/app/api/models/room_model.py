from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class RoomSchema(BaseModel):
    type: str
    owner: str
    owner_id: int
    price_per_day: float

class RoomDB(RoomSchema):
	id: int
	created_at: datetime
	updated_at: datetime

class RoomPatch(BaseModel):
	type: Optional[str] = None
	price_per_day: Optional[float] = None
