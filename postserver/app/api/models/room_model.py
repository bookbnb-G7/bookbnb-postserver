from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    type: str
    owner: str
    owner_id: int
    price_per_day: float
    lng: float
    lat: float


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
