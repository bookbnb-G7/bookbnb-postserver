from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class RoomCommentSchema(BaseModel):
    comment: str
    commentator: str
    commentator_id: int
    main_comment_id: Optional[int] = None


class RoomCommentDB(RoomCommentSchema):
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime


class RoomCommentWithAnswers(BaseModel):
    comment: RoomCommentDB
    answers: List[RoomCommentDB]


class RoomCommentsList(BaseModel):
    amount: int
    room_id: int
    comments: List[RoomCommentWithAnswers]
