from app.db import Base 
from sqlalchemy import Column, String, Integer, Float, ForeignKey

class RoomRating(Base):

	__tablename__ = 'room_ratings'

	id = Column("id", Integer, primary_key=True)
	rating = Column(Integer, nullable=False)
	room_id = Column(Integer, ForeignKey('rooms.id'))
	reviewer = Column(String(50), nullable=False)
	reviewer_id = Column(Integer, nullable=False)

	def __init__(self, rating, room_id, reviewer, reviewer_id):
		self.rating = rating
		self.room_id = room_id
		self.reviewer = reviewer
		self.reviewer_id = reviewer_id

	def serialize(self):
		return {
			'id': self.id,
			'rating': self.rating,
			'room_id': self.room_id,
			'reviewer': self.reviewer,
			'reviewer_id': self.reviewer_id
		}