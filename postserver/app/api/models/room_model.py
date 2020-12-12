from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class RoomSchema(BaseModel):
    type: str
    owner: str
    owner_uuid: int
    price_per_day: float


class RoomDB(RoomSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class RoomList(BaseModel):
    amount: int
    rooms: List[RoomDB]


class RoomPatch(BaseModel):
    type: Optional[str] = None
    price_per_day: Optional[float] = None
