from app.model.room import Room
from app.errors.http_error import NotFoundError
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from app.model.room_booking import RoomBooking
import datetime

RADIUS = 10


def validate_date_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        # Incorrect data format, should be YYYY-MM-DD
        return False


class RoomDAO:
    @classmethod
    def add_new_room(cls, db, room_args):
        new_room = Room(
            type=room_args.type,
            owner=room_args.owner,
            latitude=room_args.latitude,
            longitude=room_args.longitude,
            owner_uuid=room_args.owner_uuid,
            price_per_day=room_args.price_per_day,
        )

        db.add(new_room)
        db.commit()

        return new_room.serialize()

    @classmethod
    def get_room(cls, db, room_id):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        return room.serialize()

    @classmethod
    def delete_room(cls, db, room_id):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        db.delete(room)
        db.commit()

        return room.serialize()

    @classmethod
    def update_room(cls, db, room_id, update_args):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        # we should see if is necessary to update
        # owner and owner id. May be this should
        # be a restricted method)

        if update_args.type is not None:
            room.type = update_args.type

        if update_args.price_per_day is not None:
            room.price_per_day = update_args.price_per_day

        if update_args.latitude is not None:
            room.latitude = update_args.latitude

        if update_args.longitude is not None:
            room.longitude = update_args.longitude

        db.commit()

        return room.serialize()

    @classmethod
    def get_all_rooms(cls, db, date_begins, date_ends, longitude, latitude):

        partial_query = db.query(Room)

        # Date query
        if ((date_begins is not None) and
            (date_ends is not None) and
            (validate_date_format(date_begins)) and
            (validate_date_format(date_ends)) and
            (datetime.datetime.strptime(date_begins, '%Y-%m-%d') <= datetime.datetime.strptime(date_ends, '%Y-%m-%d'))
        ):
            date_begins = datetime.datetime.strptime(date_begins, '%Y-%m-%d')
            date_ends = datetime.datetime.strptime(date_ends, '%Y-%m-%d')
            # Get the list of room ids that are booked between the dates received
            book_list = book_list = db.query(RoomBooking) \
                .filter(((RoomBooking.date_begins <= date_ends) & 
                        (RoomBooking.date_ends >= date_begins))) \
                .distinct(RoomBooking.room_id) \
                .with_entities(RoomBooking.room_id) \
                .all()
            # Turn the list of tuples into a list
            for i in range(len(book_list)):
                book_list[i] = book_list[i][0]
            # Filter the rooms that are not booked in the range
            partial_query = partial_query.filter(~ Room.id.in_(book_list))

        # Location query
        if ((longitude is not None) and
            (latitude is not None) and
            (-180 < longitude < 180) and
            (-90 < latitude < 90)
        ):
            point = WKTElement(f'POINT({longitude} {latitude})', srid=4326)
            partial_query = partial_query.filter(func.ST_DWithin(Room.location, point, RADIUS))

        # TODO: if people != none and is number >= 0:
            # add filter capacity >= people

        rooms_list = partial_query.all()

        serialized_list = []
        for room in rooms_list:
            serialized_list.append(room.serialize())

        return serialized_list

    @classmethod
    def room_is_present(cls, db, room_id):
        room = db.query(Room).get(room_id)
        return room is not None
