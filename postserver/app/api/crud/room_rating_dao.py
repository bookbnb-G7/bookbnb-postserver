from app.db import session
from app.model.room_rating import RoomRating

class RoomRatingDAO:

	@classmethod
	def add_new_room_rating(cls, room_id, room_rating_args):
		new_room_rating = RoomRating(rating=room_rating_args.rating,
									 room_id=room_id,
			                         reviewer=room_rating_args.reviewer,
			                         reviewer_id=room_rating_args.reviewer_id)
		
		session.add(new_room_rating)
		session.commit()

		return new_room_rating.serialize()

	@classmethod
	def get_all_ratings(cls, room_id):
		rating_list = session.query(RoomRating).filter(room_id == RoomRating.room_id).all()

		serialized_list = []
		for rating in rating_list:
			serialized_list.append(rating.serialize())

		return serialized_list
	