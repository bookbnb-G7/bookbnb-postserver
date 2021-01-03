from typing import Optional
from app.db import Session, get_db
from app.api.crud.room_dao import RoomDAO
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from app.api.models.room_model import (RoomDB,
                                       RoomList,
                                       RoomPatch,
                                       RoomSchema)

router = APIRouter()


@router.post("/", response_model=RoomDB, status_code=201)
async def create_room(
        payload: RoomSchema, db: Session = Depends(get_db),
        api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_info = RoomDAO.add_new_room(db, payload)
    return room_info


@router.get("/{room_id}", response_model=RoomDB, status_code=200)
async def get_room(
        room_id: int, db: Session = Depends(get_db),
        api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_info = RoomDAO.get_room(db, room_id)
    return room_info


@router.delete("/{room_id}", response_model=RoomDB, status_code=200)
async def delete_room(
        room_id: int, db: Session = Depends(get_db),
        api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_info = RoomDAO.delete_room(db, room_id)
    return room_info


@router.patch("/{room_id}", response_model=RoomDB, status_code=200)
async def update_room(
        payload: RoomPatch, room_id: int, db: Session = Depends(get_db),
        api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_info = RoomDAO.update_room(db, room_id, payload)
    return room_info


@router.get("/", response_model=RoomList, status_code=200)
async def get_all_rooms(
        db: Session = Depends(get_db),
        api_key: Optional[str] = Header(None),
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        people: Optional[int] = None,
        owner_uuid: Optional[int] = None
):
    auth_service.verify_apy_key(api_key)
    rooms_list = RoomDAO.get_all_rooms(
        db, date_from, date_to, longitude, latitude, people, owner_uuid
    )
    amount_rooms = len(rooms_list)
    return {"amount": amount_rooms, "rooms": rooms_list}

# the query params are just normal parameters of the function that will
# be add on the next update. By now, this function returns all rooms
