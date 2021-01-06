from app.db import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class RoomComment(Base):

    __tablename__ = "room_comments"

    id = Column("id", Integer, primary_key=True)
    comment = Column(String(500), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    commentator = Column(String(50), nullable=False)
    commentator_id = Column(Integer, nullable=False)
    main_comment_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, comment, commentator, room_id, commentator_id, main_comment_id):
        self.comment = comment
        self.room_id = room_id
        self.commentator = commentator
        self.commentator_id = commentator_id
        self.main_comment_id = main_comment_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "room_id": self.room_id,
            "commenter": self.commenter,
            "commenter_id": self.commenter_id,
            "main_comment_id": self.main_comment_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_from(self, room_id):
        return self.room_id == room_id

    def is_answer(self):
        return self.main_comment_id is not None
