from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class RoomReviewSchema(BaseModel):
    review: str
    reviewer: str
    reviewer_id: int


class RoomReviewDB(RoomReviewSchema):
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime


class RoomReviewList(BaseModel):
    amount: int
    room_id: int
    reviews: List[RoomReviewDB]
