from app.db import Session, get_db 
from fastapi import APIRouter, HTTPException, Depends

from app.api.crud.room_dao import RoomDAO
from app.api.crud.room_rating_dao import RoomRatingDAO
from app.api.crud.room_review_dao import RoomReviewDAO

from app.api.models.room_model import RoomSchema, RoomDB
from app.api.models.room_rating_model import RoomRatingSchema, RoomRatingDB, RoomRatingList
from app.api.models.room_review_model import RoomReviewSchema, RoomReviewDB, RoomReviewList

router = APIRouter()

@router.post('/', response_model=RoomDB, status_code=201)
async def create_room(payload: RoomSchema, db: Session = Depends(get_db)):
	room_info = RoomDAO.add_new_room(db, payload)
	return room_info

@router.post('/{room_id}/ratings', response_model=RoomRatingDB, status_code=201)
async def rate_room(payload: RoomRatingSchema, room_id: int, db: Session = Depends(get_db)):
	room_rating_info = RoomRatingDAO.add_new_room_rating(db, room_id, payload)
	return room_rating_info

@router.post('/{room_id}/reviews', response_model=RoomReviewDB, status_code=201)
async def review_room(payload: RoomReviewSchema, room_id: int, db: Session = Depends(get_db)):
	room_review_info = RoomReviewDAO.add_new_room_review(db, room_id, payload)
	return room_review_info

@router.get('/{room_id}', response_model=RoomDB, status_code=200)
async def get_room(room_id: int,  db: Session = Depends(get_db)):
	room_info = RoomDAO.get_room(db, room_id)
	return room_info

@router.get('/{room_id}/reviews/{review_id}', response_model=RoomReviewDB, status_code=200)
async def get_room_review(room_id: int, review_id: int, db: Session = Depends(get_db)):
	room_review_info = RoomReviewDAO.get_room_review(db, room_id, review_id)
	return room_review_info

@router.get('/{room_id}/ratings/{rating_id}', response_model=RoomRatingDB, status_code=200)
async def get_room_rating(room_id: int, rating_id: int, db: Session = Depends(get_db)):
	room_rating_info = RoomRatingDAO.get_room_rating(db, room_id, rating_id)
	return room_rating_info

@router.get('/{room_id}/ratings', response_model=RoomRatingList, status_code=200)
async def get_all_room_reviews(room_id: int, db: Session = Depends(get_db)):
	room_ratings_list = RoomRatingDAO.get_all_ratings(db, room_id)
	return { 'room_id':room_id, 'ratings': room_ratings_list }

@router.get('/{room_id}/reviews', response_model=RoomReviewList, status_code=200)
async def get_all_room_reviews(room_id: int,  db: Session = Depends(get_db)):
	room_reviews_list = RoomReviewDAO.get_all_reviews(db, room_id)
	return { 'room_id':room_id, 'reviews': room_reviews_list }
