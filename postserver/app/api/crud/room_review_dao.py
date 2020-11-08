from app.model.room_review import RoomReview

class RoomReviewDAO:

	@classmethod
	def add_new_room_review(cls, db, room_id, room_review_args):
		new_room_review = RoomReview(review=room_review_args.review,
									 room_id=room_id,
			                         reviewer=room_review_args.reviewer,
			                         reviewer_id=room_review_args.reviewer_id)
		
		db.add(new_room_review)
		db.commit()

		return new_room_review.serialize()
	
	
	@classmethod
	def get_all_reviews(cls, db, room_id):
		review_list = db.query(RoomReview).filter(room_id == RoomReview.room_id).all()

		serialized_list = []
		for review in review_list:
			serialized_list.append(review.serialize())

		return serialized_list


	@classmethod
	def get_room_review(cls, db, room_id, review_id):
		room_review = db.query(RoomReview).get(review_id)

		# this should return an error in case of  
		# the rating do not for the specified room

		return room_review.serialize()


	@classmethod
	def delete_room_review(cls, db, room_id, review_id):
		room_review = db.query(RoomReview).get(review_id)
		
		db.delete(room_review)
		db.commit()

		# this should return an error in case of  
		# the rating do not for the specified room

		return room_review.serialize()


	@classmethod
	def update_room_review(cls, db, room_id, review_id, update_args):
		room_review = db.query(RoomReview).get(review_id)

		# we should see if is necessary to update
		# owner and owner id. May be this should
		# be a restricted method

		if update_args.review is not None:
			room_review.review = update_args.review
			
		db.commit()

		return room_review.serialize()
