import json
import pytest

room_id = 1

test_room_payload = {
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_uuid": 1,
    "latitude": 1.0,
    "longitude": 2.0,
    "price_per_day": 1000.0,
    "capacity": 7,
}

test_room_booking_payload = {
    "user_id": 1,
    "date_ends": "2020-12-30",
    "date_begins": "2020-12-15",
    "amount_of_people": 3
}

test_another_room_booking_payload = {
    "user_id": 1,
    "date_ends": "2020-12-14",
    "date_begins": "2020-12-10",
    "amount_of_people": 3
}

header = {"api-key": "ULTRAMEGAFAKEAPIKEY"}


def _create_room(test_app):
    test_app.post(url="/rooms/",
                  headers=header,
                  data=json.dumps(test_room_payload))


def _delete_room(test_app):
    test_app.delete(url="/rooms/" + str(room_id),
                    headers=header)


@pytest.mark.usefixtures("test_app")
class TestRoomBooking:
    def test_book_an_existing_room(self, test_app):
        _create_room(test_app)

        response = test_app.post(
            url="/rooms/" + str(room_id) + "/bookings/",
            headers=header,
            data=json.dumps(test_room_booking_payload),
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["room_id"] == room_id
        assert response_json["user_id"] == test_room_booking_payload["user_id"]
        assert response_json["date_ends"] == test_room_booking_payload["date_ends"]
        assert response_json["total_price"] == 15 * test_room_payload["price_per_day"]
        assert response_json["date_begins"] == test_room_booking_payload["date_begins"]

    def test_book_a_room_without_api_key(self, test_app):
        response = test_app.post(
            url="/rooms/" + str(room_id) + "/bookings/",
            data=json.dumps(test_room_booking_payload),
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_book_an_non_existent_room(self, test_app):
        not_existent_room_id = 25

        response = test_app.post(
            url="/rooms/" + str(not_existent_room_id) + "/bookings/",
            headers=header,
            data=json.dumps(test_room_booking_payload),
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_an_existing_room_booking(self, test_app):
        rating_id = 1

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/bookings/" + str(rating_id),
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["room_id"] == room_id
        assert response_json["user_id"] == test_room_booking_payload["user_id"]
        assert response_json["date_ends"] == test_room_booking_payload["date_ends"]
        assert response_json["total_price"] == 15 * test_room_payload["price_per_day"]
        assert response_json["date_begins"] == test_room_booking_payload["date_begins"]

    def test_get_an_non_existent_room_rating(self, test_app):
        not_existent_room_booking_id = 25

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/bookings/" + str(not_existent_room_booking_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room booking not found"

    def test_get_a_room_booking_from_a_non_existen_room(self, test_app):
        booking_id = 1
        not_existent_room_id = 25

        response = test_app.get(
            url="/rooms/" + str(not_existent_room_id) + "/bookings/" + str(booking_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_all_existing_room_ratings_from_room(self, test_app):
        # add another rating to the existing room
        test_app.post(
            url="/rooms/" + str(room_id) + "/bookings/",
            headers=header,
            data=json.dumps(test_another_room_booking_payload)
        )

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/bookings/",
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        frt_rating = response_json["bookings"][0]
        snd_rating = response_json["bookings"][1]

        # control that first rating is correct
        assert frt_rating["id"] == 1
        assert frt_rating["room_id"] == room_id
        assert frt_rating["user_id"] == test_room_booking_payload["user_id"]
        assert frt_rating["date_ends"] == test_room_booking_payload["date_ends"]
        assert frt_rating["total_price"] == 15 * test_room_payload["price_per_day"]
        assert frt_rating["date_begins"] == test_room_booking_payload["date_begins"]

        # control that second rating is correct
        assert snd_rating["id"] == 2
        assert snd_rating["room_id"] == room_id
        assert snd_rating["total_price"] == 4 * test_room_payload["price_per_day"]
        assert snd_rating["user_id"] == test_another_room_booking_payload["user_id"]
        assert snd_rating["date_ends"] == test_another_room_booking_payload["date_ends"]
        assert snd_rating["date_begins"] == test_another_room_booking_payload["date_begins"]

        # controlas that rating list metadata is correct
        assert response_json["amount"] == 2
        assert response_json["room_id"] == room_id

    def test_delete_a_non_existent_room_booking(self, test_app):
        non_existent_room_rating_id = 25

        response = test_app.delete(
            url="/rooms/" + str(room_id) + "/bookings/" + str(non_existent_room_rating_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room booking not found"

    def test_delete_a_room_rating_from_a_non_existent_room(self, test_app):
        rating_id = 1
        non_existent_room_id = 25

        response = test_app.delete(
            url="/rooms/" + str(non_existent_room_id) + "/bookings/" + str(rating_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_delete_existing_room_ratings(self, test_app):
        booking_1_id = 1
        booking_2_id = 2

        response_1 = test_app.delete(
            url="/rooms/" + str(room_id) + "/bookings/" + str(booking_1_id),
            headers=header
        )

        response_2 = test_app.delete(
            url="/rooms/" + str(room_id) + "/bookings/" + str(booking_2_id),
            headers=header
        )

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        response_json_1 = response_1.json()
        response_json_2 = response_2.json()

        # control that first rating is correct
        assert response_json_1["id"] == 1
        assert response_json_1["room_id"] == room_id
        assert response_json_1["user_id"] == test_room_booking_payload["user_id"]
        assert response_json_1["date_ends"] == test_room_booking_payload["date_ends"]
        assert response_json_1["total_price"] == 15 * test_room_payload["price_per_day"]
        assert response_json_1["date_begins"] == test_room_booking_payload["date_begins"]

        # control that second rating is correct
        assert response_json_2["id"] == 2
        assert response_json_2["room_id"] == room_id
        assert response_json_2["total_price"] == 4 * test_room_payload["price_per_day"]
        assert response_json_2["user_id"] == test_another_room_booking_payload["user_id"]
        assert response_json_2["date_ends"] == test_another_room_booking_payload["date_ends"]
        assert response_json_2["date_begins"] == test_another_room_booking_payload["date_begins"]

        _delete_room(test_app)
