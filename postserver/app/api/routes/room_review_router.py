from app.db import Session, get_db 
from fastapi import APIRouter, HTTPException, Depends

from app.api.crud.room_review_dao import RoomReviewDAO

from app.api.models.room_review_model import RoomReviewSchema, RoomReviewDB, \
											 RoomReviewList, RoomReviewPatch

router = APIRouter()

@router.post('', response_model=RoomReviewDB, status_code=201)
async def review_room(payload: RoomReviewSchema, room_id: int, db: Session = Depends(get_db)):
	room_review_info = RoomReviewDAO.add_new_room_review(db, room_id, payload)
	return room_review_info

@router.get('/', response_model=RoomReviewList, status_code=200)
async def get_all_room_reviews(room_id: int,  db: Session = Depends(get_db)):
	room_reviews_list = RoomReviewDAO.get_all_reviews(db, room_id)
	return { 'room_id':room_id, 'reviews': room_reviews_list }

@router.get('/{review_id}', response_model=RoomReviewDB, status_code=200)
async def get_room_review(room_id: int, review_id: int, db: Session = Depends(get_db)):
	room_review_info = RoomReviewDAO.get_room_review(db, room_id, review_id)
	return room_review_info

@router.delete('/{review_id}', response_model=RoomReviewDB, status_code=200)
async def delete_room_review(room_id: int, review_id: int, db: Session = Depends(get_db)):
	room_review_info = RoomReviewDAO.delete_room_review(db, room_id, review_id)
	return room_review_info

@router.patch('/{review_id}', response_model=RoomReviewDB, status_code=200)
async def update_room_review(payload: RoomReviewPatch, room_id: int, review_id: int, db: Session = Depends(get_db)):
	room_review_info = RoomReviewDAO.update_room_review(db, room_id, review_id, payload)
	return room_review_info