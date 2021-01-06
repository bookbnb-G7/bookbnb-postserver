from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class RoomSchema(BaseModel):
    id: int
    type: str
    owner: str
    owner_uuid: int
    latitude: float
    longitude: float
    price_per_day: int
    location: str
    capacity: int


class RoomDB(RoomSchema):
    created_at: datetime
    updated_at: datetime


class RoomList(BaseModel):
    amount: int
    rooms: List[RoomDB]


class RoomPatch(BaseModel):
    type: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price_per_day: Optional[int] = None
