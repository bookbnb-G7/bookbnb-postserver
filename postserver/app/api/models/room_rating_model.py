from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

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
	room_id: int
	ratings: List[RoomRatingDB]

class RoomRatingPatch(BaseModel):
	rating: Optional[int] = None
	