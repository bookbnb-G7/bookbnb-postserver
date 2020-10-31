"""

from app.model.room import Room
from app.model.room_rating import RoomRating
from app.model.room_review import RoomReview

class Parser:	
	def get_room(self, room_payload):
		price_per_day = room_payload.price_per_day
		accommodation_type = room_payload.accommodation_type

		return Room(accommodation_type, price_per_day)

	
	def get_room_rating(self, room_rating_payload, room_id):
		rating = room_rating_payload.rating
		reviewer = room_rating_payload.reviewer
		reviewer_id = room_rating_payload.reviewer_id

		return RoomRating(rating, reviewer, room_id, reviewer_id)

	def get_room_review(self, room_review_payload, room_id):
		review = room_review_payload.review
		reviewer = room_review_payload.reviewer
		reviewer_id = room_review_payload.reviewer_id

		return RoomReview(review, reviewer, room_id, reviewer_id)
"""