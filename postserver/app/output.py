from app.model.room_rating import RoomRating
from app.model.room_review import RoomReview

class Output:
	def reply_room_creation(self, room_id, room):
		print('entre!')
		review_response = {
			'id': room_id,
			'price_per_day': room.price_per_day,
			'accommodation_type': room.accommodation_type
		}

		return review_response

	def reply_room_rating_creation(self, rating_id, room_rating):
		rating_response = {
			'id': rating_id,
			'rating': room_rating.rating,
    		'room_id': room_rating.room_id,
    		'reviewer': room_rating.reviewer,
    		'reviewer_id': room_rating.reviewer_id
		}

		return rating_response

	def reply_room_review_creation(self, review_id, room_review):
		review_response = {
			'id': review_id,
			'review': room_review.review,
    		'room_id': room_review.room_id,
    		'reviewer': room_review.reviewer,
    		'reviewer_id': room_review.reviewer_id
		}

		return review_response


