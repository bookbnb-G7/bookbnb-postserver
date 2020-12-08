from typing import Optional
from app.db import Session, get_db
from app.services.auth import auth_service 
from fastapi import APIRouter, Depends, Header
from app.api.crud.room_rating_dao import RoomRatingDAO
from app.api.models.room_rating_model import (RoomRatingDB, 
                                              RoomRatingList,
                                              RoomRatingPatch,
                                              RoomRatingSchema)

router = APIRouter()

@router.post("/", response_model=RoomRatingDB, status_code=201)
async def rate_room(
    payload: RoomRatingSchema, room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_rating_info = RoomRatingDAO.add_new_room_rating(db, room_id, payload)
    return room_rating_info


@router.get("/", response_model=RoomRatingList, status_code=200)
async def get_all_room_ratings(
    room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_ratings_list = RoomRatingDAO.get_all_ratings(db, room_id)
    amount_ratings = len(room_ratings_list)
    return {"room_id": room_id, "amount": amount_ratings, "ratings": room_ratings_list}


@router.get("/{rating_id}", response_model=RoomRatingDB, status_code=200)
async def get_room_rating(
    room_id: int, rating_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_rating_info = RoomRatingDAO.get_room_rating(db, room_id, rating_id)
    return room_rating_info


@router.delete("/{rating_id}", response_model=RoomRatingDB, status_code=200)
async def delete_room_rating(
    room_id: int, rating_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_rating_info = RoomRatingDAO.delete_room_rating(db, room_id, rating_id)
    return room_rating_info


@router.patch("/{rating_id}", response_model=RoomRatingDB, status_code=200)
async def update_room_rating(
    payload: RoomRatingPatch, room_id: int, rating_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_rating_info = RoomRatingDAO.update_room_rating(db, room_id, rating_id, payload)
    return room_rating_info
