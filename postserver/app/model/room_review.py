from app.db import Base 
from sqlalchemy import Column, String, Integer, Float, ForeignKey

class RoomReview(Base):

	__tablename__ = 'room_reviews'

	id = Column("id", Integer, primary_key=True)
	review = Column(String(500), nullable=False)
	room_id = Column(Integer, ForeignKey('rooms.id'))
	reviewer = Column(String(50), nullable=False)
	reviewer_id = Column(Integer, nullable=False)

	def __init__(self, review, reviewer, room_id, reviewer_id):
		self.review = review
		self.room_id = room_id
		self.reviewer = reviewer
		self.reviewer_id = reviewer_id

	def serialize(self):
		return {
			'id': self.id,
			'review': self.review,
			'room_id': self.room_id,
			'reviewer': self.reviewer,
			'reviewer_id': self.reviewer_id
		}