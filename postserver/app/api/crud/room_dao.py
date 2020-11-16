from app.model.room import Room
from app.errors.error import NotFoundError

class RoomDAO:

	@classmethod
	def add_new_room(cls, db, room_args): 
		new_room = Room(type=room_args.type,
			            owner=room_args.owner,
			            owner_id=room_args.owner_id,
			            price_per_day=room_args.price_per_day)

		db.add(new_room)
		db.commit()

		return new_room.serialize()


	@classmethod
	def get_room(cls, db, room_id):
		room = db.query(Room).get(room_id)

		if room is None: 
			raise NotFoundError()

		return room.serialize()


	@classmethod
	def delete_room(cls, db, room_id):
		room = db.query(Room).get(room_id)

		if room is None:
			raise NotFoundError()
		
		db.delete(room)
		db.commit()

		return room.serialize()

	
	@classmethod
	def update_room(cls, db, room_id, update_args):
		room = db.query(Room).get(room_id)

		if room is None:
			raise NotFoundError()

		# we should see if is necessary to update
		# owner and owner id. May be this should
		# be a restricted method)

		if update_args.type is not None:
			room.type = update_args.type

		if update_args.price_per_day is not None:
			room.price_per_day = update_args.price_per_day
	       
		db.commit()

		return room.serialize()


	@classmethod
	def get_all_rooms(cls, db):
		rooms_list = db.query(Room).all()

		serialized_list = []
		for room in rooms_list:
			serialized_list.append(room.serialize())

		return serialized_list
