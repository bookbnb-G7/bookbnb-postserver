from typing import List
from datetime import datetime
from pydantic import BaseModel

class RoomPhotoSchema(BaseModel):
	url: str
	firebase_id: int 

class RoomPhotoDB(RoomPhotoSchema):
	id: int
	url: str
	room_id: int
	firebase_id: int 
	created_at: datetime
	updated_at: datetime

class RoomPhotoList(BaseModel):
	amount: int 
	room_id: int
	room_photos: List[RoomPhotoDB]