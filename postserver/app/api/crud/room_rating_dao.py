from app.model.room_rating import RoomRating

class RoomRatingDAO:

	@classmethod
	def add_new_room_rating(cls, db, room_id, room_rating_args):
		new_room_rating = RoomRating(rating=room_rating_args.rating,
									 room_id=room_id,
			                         reviewer=room_rating_args.reviewer,
			                         reviewer_id=room_rating_args.reviewer_id)
		
		db.add(new_room_rating)
		db.commit()

		return new_room_rating.serialize()

	
	@classmethod
	def get_all_ratings(cls, db, room_id):
		rating_list = db.query(RoomRating).filter(room_id == RoomRating.room_id).all()

		serialized_list = []
		for rating in rating_list:
			serialized_list.append(rating.serialize())

		return serialized_list
	

	@classmethod
	def get_room_rating(cls, db, room_id, rating_id):
		room_rating = db.query(RoomRating).get(rating_id)

		# this should return an error in case of  
		# the rating do not for the specified room

		return room_rating.serialize()


	@classmethod
	def delete_room_rating(cls, db, room_id, rating_id):
		room_rating = db.query(RoomRating).get(rating_id)
		
		db.delete(room_rating)
		db.commit()

		# this should return an error in case of  
		# the rating do not for the specified room
		# (one way of doing this is to control ID on
		# DB delete query) 
		# Ex. (Room.ID == room_id and 
		#	 RoomRating.id == room_rating_id)

		return room_rating.serialize()


	@classmethod
	def update_room_rating(cls, db, room_id, rating_id, update_args):
		room_rating = db.query(RoomRating).get(rating_id)

		# we should see if is necessary to update
		# owner and owner id. May be this should
		# be a restricted method

		if update_args.rating is not None:
			room_rating.rating = update_args.rating

		db.commit()

		return room_rating.serialize()
