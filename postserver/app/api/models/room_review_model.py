from pydantic import BaseModel

class RoomReviewSchema(BaseModel):
	review: str 
	reviewer: str
	reviewer_id: int

class RoomReviewDB(RoomReviewSchema):
	id: int
	room_id: int