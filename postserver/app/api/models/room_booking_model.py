from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime


class RoomBookingSchema(BaseModel):
    id: int
    user_id: int
    date_ends: date
    date_begins: date
    amount_of_people: int
    status: int


class RoomBookingDB(RoomBookingSchema):
    room_id: int
    total_price: float
    created_at: datetime
    updated_at: datetime


class RoomBookingList(BaseModel):
    amount: int
    room_id: int
    bookings: List[RoomBookingDB]


class RoomBookingPatch(BaseModel):
    status: Optional[int] = None
