from typing import Optional
from app.db import Session, get_db
from app.services.auth import auth_service 
from fastapi import APIRouter, Depends, Header
from app.api.crud.room_review_dao import RoomReviewDAO
from app.api.models.room_review_model import (RoomReviewDB, 
                                              RoomReviewList,
                                              RoomReviewPatch,
                                              RoomReviewSchema)

router = APIRouter()


@router.post("/", response_model=RoomReviewDB, status_code=201)
async def review_room(
    payload: RoomReviewSchema, room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_review_info = RoomReviewDAO.add_new_room_review(db, room_id, payload)
    return room_review_info


@router.get("/", response_model=RoomReviewList, status_code=200)
async def get_all_room_reviews(
    room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_reviews_list = RoomReviewDAO.get_all_reviews(db, room_id)
    amount_reviews = len(room_reviews_list)
    return {"room_id": room_id, "amount": amount_reviews, "reviews": room_reviews_list}


@router.get("/{review_id}", response_model=RoomReviewDB, status_code=200)
async def get_room_review(
    room_id: int, review_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_review_info = RoomReviewDAO.get_room_review(db, room_id, review_id)
    return room_review_info


@router.delete("/{review_id}", response_model=RoomReviewDB, status_code=200)
async def delete_room_review(
    room_id: int, review_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_review_info = RoomReviewDAO.delete_room_review(db, room_id, review_id)
    return room_review_info


@router.patch("/{review_id}", response_model=RoomReviewDB, status_code=200)
async def update_room_review(
    payload: RoomReviewPatch, room_id: int, review_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_review_info = RoomReviewDAO.update_room_review(db, room_id, review_id, payload)
    return room_review_info
