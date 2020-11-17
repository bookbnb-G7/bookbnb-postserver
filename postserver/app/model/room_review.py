from app.db import Base 
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime

class RoomReview(Base):

	__tablename__ = 'room_reviews'

	id = Column("id", Integer, primary_key=True)
	review = Column(String(500), nullable=False)
	room_id = Column(Integer, ForeignKey('rooms.id'))
	reviewer = Column(String(50), nullable=False)
	reviewer_id = Column(Integer, nullable=False)

	created_at = Column(DateTime, nullable=False)
	updated_at = Column(DateTime, nullable=False)

	def __init__(self, review, reviewer, room_id, reviewer_id):
		self.review = review
		self.room_id = room_id
		self.reviewer = reviewer
		self.reviewer_id = reviewer_id
		self.created_at = datetime.now()
		self.updated_at = datetime.now()

	def serialize(self):
		return {
			'id': self.id,
			'review': self.review,
			'room_id': self.room_id,
			'reviewer': self.reviewer,
			'reviewer_id': self.reviewer_id,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}

	def is_from(self, room_id):
		return self.room_id == room_id