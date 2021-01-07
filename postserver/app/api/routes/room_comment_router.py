from typing import Optional
from app.db import Session, get_db
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from app.api.crud.room_comment_dao import RoomCommentDAO
from app.api.models.room_comment_model import (RoomCommentSchema,
                                               RoomCommentDB,
                                               RoomCommentsList)

router = APIRouter()


@router.post("", response_model=RoomCommentDB, status_code=201)
async def comment_room(
    payload: RoomCommentSchema, room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_comment = RoomCommentDAO.add_new_comment(db, room_id, payload)
    return room_comment


@router.get("", response_model=RoomCommentsList, status_code=200)
async def get_all_room_comments(
    room_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_comments_list = RoomCommentDAO.get_all_comments(db, room_id)
    amount_comments = len(room_comments_list)
    return {
        "room_id": room_id,
        "amount": amount_comments,
        "comments": room_comments_list
    }


@router.get("/{comment_id}", response_model=RoomCommentDB, status_code=200)
async def get_room_comment(
    room_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_comment = RoomCommentDAO.get_comment(db,
                                              room_id,
                                              comment_id)
    return room_comment


@router.delete("/{comment_id}", response_model=RoomCommentDB, status_code=200)
async def delete_room_comment(
    room_id: int, comment_id: int, db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    room_comment = RoomCommentDAO.delete_comment(db, room_id, comment_id)
    return room_comment
