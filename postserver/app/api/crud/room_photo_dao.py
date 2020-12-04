from app.model.room_photo import RoomPhoto
from app.errors.http_error import NotFoundError


class RoomPhotoDAO:
    @classmethod
    def add_new_room_photo(cls, db, room_id, room_photo_args):
        new_room_photo = RoomPhoto(
            room_id=room_id,
            url=room_photo_args.url,
            firebase_id=room_photo_args.firebase_id,
        )

        db.add(new_room_photo)
        db.commit()

        return new_room_photo.serialize()

    @classmethod
    def get_room_photo(cls, db, firebase_id):
        room_photo = (
            db.query(RoomPhoto).filter(RoomPhoto.firebase_id == firebase_id).first()
        )

        if room_photo is None:
            raise NotFoundError("room_photo")

        return room_photo.serialize()

    @classmethod
    def delete_room_photo(cls, db, firebase_id):
        room_photo = (
            db.query(RoomPhoto).filter(RoomPhoto.firebase_id == firebase_id).first()
        )

        if room_photo is None:
            raise NotFoundError("room_photo")

        db.delete(room_photo)
        db.commit()

        return room_photo.serialize()

    @classmethod
    def get_all_room_photos(cls, db, room_id):
        room_photos_list = (
            db.query(RoomPhoto).filter(RoomPhoto.room_id == room_id).all()
        )

        serialized_list = []
        for room_photo in room_photos_list:
            serialized_list.append(room_photo.serialize())

        return serialized_list
