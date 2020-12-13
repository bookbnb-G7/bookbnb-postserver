from typing import List
from pydantic import BaseModel
from datetime import date, datetime


class RoomBookingSchema(BaseModel):
    user_id: int
    date_ends: date
    date_begins: date
    amount_of_people: int


class RoomBookingDB(RoomBookingSchema):
    id: int
    room_id: int
    total_price: float
    created_at: datetime
    updated_at: datetime


class RoomBookingList(BaseModel):
    amount: int
    rooms: List[RoomBookingDB]
