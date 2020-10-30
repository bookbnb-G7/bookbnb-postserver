from app.io.parser import Parser
from app.io.output import Output

from fastapi import APIRouter, HTTPException

from app.api.crud import room_crud as room_controller
from app.api.crud import room_rating_crud as room_rating_controller
from app.api.crud import room_review_crud as room_review_controller

from app.api.models.room_model import RoomSchema, RoomDB
from app.api.models.room_rating_model import RoomRatingSchema, RoomRatingDB
from app.api.models.room_review_model import RoomReviewSchema, RoomReviewDB

output = Output()
parser = Parser()
router = APIRouter()

@router.post('/', response_model=RoomDB, status_code=200)
async def create_room(payload: RoomSchema):
	room = parser.get_room(payload)
	room_id = await room_controller.create(room)
	return output.reply_room_creation(room_id, room)

@router.post('/{room_id}/ratings', response_model=RoomRatingDB, status_code=201)
async def rate_room(payload: RoomRatingSchema, room_id: int):
	room_rating = parser.get_room_rating(payload, room_id)
	rating_id = await room_rating_controller.create(room_rating)
	return output.reply_room_rating_creation(rating_id, room_rating)

@router.post('/{room_id}/reviews', response_model=RoomReviewDB, status_code=201)
async def review_room(payload: RoomReviewSchema, room_id: int):
	room_review = parser.get_room_review(payload, room_id)
	review_id = await room_review_controller.create(room_review)
	return output.reply_room_review_creation(review_id, room_review)
