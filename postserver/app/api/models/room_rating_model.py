from typing import List
from datetime import datetime
from pydantic import BaseModel


class RoomRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: int


class RoomRatingDB(RoomRatingSchema):
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime


class RoomRatingList(BaseModel):
    amount: int
    room_id: int
    ratings: List[RoomRatingDB]
