from app.api.crud.room_dao import RoomDAO
from app.model.room_booking import RoomBooking
from app.errors.http_error import NotFoundError
from app.errors.bookbnb_error import RoomAlreadyBookedError, NoRelationError


class RoomBookingDAO:
    @classmethod
    def add_new_room_booking(cls, db, room_id, room_booking_args):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room = RoomDAO.get_room(db, room_id)

        # add validation about capacity

        booking_ends = room_booking_args.date_ends
        booking_begins = room_booking_args.date_begins

        bookings_on_same_date = db.query(RoomBooking) \
            .filter(RoomBooking.room_id == room_id) \
            .filter(RoomBooking.date_begins <= booking_begins,
                    RoomBooking.date_ends >= booking_begins,
                    RoomBooking.date_begins <= booking_ends,
                    RoomBooking.date_ends >= booking_ends) \
            .count()

        if bookings_on_same_date > 0:
            raise RoomAlreadyBookedError()

        booking_days = (booking_ends - booking_begins).days
        total_price = booking_days * room['price_per_day']

        new_room_booking = RoomBooking(
            room_id=room_id,
            date_ends=booking_ends,
            date_begins=booking_begins,
            total_price = total_price,
            user_id=room_booking_args.user_id,
            amount_of_people=room_booking_args.amount_of_people
        )

        db.add(new_room_booking)
        db.commit()

        return new_room_booking.serialize()

    @classmethod
    def get_room_booking(cls, db, room_id, booking_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_booking = db.query(RoomBooking)\
                         .get(booking_id)

        if room_booking is None:
            raise NotFoundError("room booking")

        if not room_booking.is_from(room_id):
            raise NoRelationError("room", "room booking")

        return room_booking.serialize()

    @classmethod
    def get_all_bookings(cls, db, room_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_bookings_list = db.query(RoomBooking)\
                               .filter(RoomBooking.room_id == room_id)

        serialized_list = []
        for booking in room_bookings_list:
            serialized_list.append(booking.serialize())

        return serialized_list

    @classmethod
    def delete_room_booking(cls, db, room_id, booking_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_booking = db.query(RoomBooking)\
                         .get(booking_id)

        if room_booking is None:
            raise NotFoundError("room booking")

        if not room_booking.is_from(room_id):
            raise NoRelationError("room", "room booking")

        db.delete(room_booking)
        db.commit()

        return room_booking.serialize()
