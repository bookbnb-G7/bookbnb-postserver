from app.api.crud.room_dao import RoomDAO
from app.model.room_booking import RoomBooking
from app.errors.http_error import NotFoundError
from app.errors.bookbnb_error import RoomAlreadyBookedError, NoRelationError


class RoomBookingDAO:
    @classmethod
    def add_new_room_booking(cls, db, room_id, room_booking_args):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        booking_to = room_booking_args.date_to
        booking_from = room_booking_args.date_from

        bookings_on_same_date = cls.bookings_on_same_date(db, room_id, booking_from, booking_to)

        if bookings_on_same_date > 0:
            raise RoomAlreadyBookedError()

        new_room_booking = RoomBooking(
            id=room_booking_args.id,
            room_id=room_id,
            date_to=booking_to,
            date_from=booking_from,
        )

        db.add(new_room_booking)
        db.commit()

        return new_room_booking.serialize()

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

    @classmethod
    def bookings_on_same_date(cls, db, room_id, date_from, date_to):

        bookings_on_same_date_1 = db.query(RoomBooking) \
            .filter(RoomBooking.room_id == room_id) \
            .filter(RoomBooking.date_from >= date_from,
                    RoomBooking.date_to <= date_to) \
            .count()

        bookings_on_same_date_2 = db.query(RoomBooking) \
            .filter(RoomBooking.room_id == room_id) \
            .filter(RoomBooking.date_from <= date_from,
                    RoomBooking.date_to >= date_from) \
            .count()

        bookings_on_same_date_3 = db.query(RoomBooking) \
            .filter(RoomBooking.room_id == room_id) \
            .filter(RoomBooking.date_from <= date_to,
                    RoomBooking.date_to >= date_to)\
            .count()

        return (bookings_on_same_date_1 + bookings_on_same_date_2 + bookings_on_same_date_3)
