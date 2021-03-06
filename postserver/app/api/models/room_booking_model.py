from typing import List
from pydantic import BaseModel
from datetime import date, datetime


class RoomBookingSchema(BaseModel):
    id: int
    date_to: date
    date_from: date


class RoomBookingDB(RoomBookingSchema):
    room_id: int
    created_at: datetime
    updated_at: datetime
