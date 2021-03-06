from typing import Optional
from app.db import Session, get_db
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from app.api.crud.room_booking_dao import RoomBookingDAO
from app.api.models.room_booking_model import RoomBookingDB, RoomBookingSchema

router = APIRouter()


@router.post("", response_model=RoomBookingDB, status_code=201)
async def book_room(
    room_id: int, payload: RoomBookingSchema,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_booking_info = RoomBookingDAO.add_new_room_booking(db, room_id, payload)
    return room_booking_info


@router.delete("/{room_booking_id}", response_model=RoomBookingDB, status_code=200)
async def delete_room_booking(
    room_id: int, room_booking_id: int,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_booking_info = RoomBookingDAO.delete_room_booking(db, room_id, room_booking_id)
    return room_booking_info
