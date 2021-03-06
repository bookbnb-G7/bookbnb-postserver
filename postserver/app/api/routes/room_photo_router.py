from typing import Optional
from app.db import Session, get_db
from app.services.auth import auth_service 
from fastapi import APIRouter, Depends, Header
from app.api.crud.room_photo_dao import RoomPhotoDAO
from app.api.models.room_photo_model import (RoomPhotoDB, 
                                             RoomPhotoList,
                                             RoomPhotoSchema)

router = APIRouter()


@router.post("", response_model=RoomPhotoDB, status_code=201)
async def new_room_photo(
    payload: RoomPhotoSchema, room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_photo_info = RoomPhotoDAO.add_new_room_photo(db, room_id, payload)
    return room_photo_info


@router.get("/{firebase_id}", response_model=RoomPhotoDB, status_code=200)
async def get_room_photo(
    firebase_id: int, room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_photo_info = RoomPhotoDAO.get_room_photo(db, room_id, firebase_id)
    return room_photo_info


@router.delete("/{firebase_id}", response_model=RoomPhotoDB, status_code=200)
async def delete_room_photo(
    firebase_id: int, room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_photo_info = RoomPhotoDAO.delete_room_photo(db, room_id, firebase_id)
    return room_photo_info


@router.get("", response_model=RoomPhotoList, status_code=200)
async def get_all_room_photos(
    room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_photos_list = RoomPhotoDAO.get_all_room_photos(db, room_id)
    amount_room_photos = len(room_photos_list)
    return {
        "amount": amount_room_photos,
        "room_id": room_id,
        "room_photos": room_photos_list,
    }
