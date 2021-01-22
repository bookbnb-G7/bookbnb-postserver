import json
import pytest

room_id = 1

test_room_payload = {
    "id": 1,
    "title": "THE ROOM",
    "description": "You are tearing me apart Lisa",
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_uuid": 1,
    "latitude": 1.0,
    "longitude": 2.0,
    "price_per_day": 1000.0,
    "location": "USA",
    "capacity": 7,
}

test_room_booking_payload = {
    "id": 1,
    "date_to": "2020-12-30",
    "date_from": "2020-12-15",
}

test_another_room_booking_payload = {
    "id": 2,
    "date_to": "2020-12-14",
    "date_from": "2020-12-10",
}

header = {"api-key": "ULTRAMEGAFAKEAPIKEY"}


def _create_room(test_app):
    test_app.post(url="/rooms",
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
            url="/rooms/" + str(room_id) + "/bookings",
            headers=header,
            data=json.dumps(test_room_booking_payload),
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["room_id"] == room_id
        assert response_json["date_to"] == test_room_booking_payload["date_to"]
        assert response_json["date_from"] == test_room_booking_payload["date_from"]

    def test_book_a_room_without_api_key(self, test_app):
        response = test_app.post(
            url="/rooms/" + str(room_id) + "/bookings",
            data=json.dumps(test_room_booking_payload),
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_book_an_non_existent_room(self, test_app):
        not_existent_room_id = 25

        response = test_app.post(
            url="/rooms/" + str(not_existent_room_id) + "/bookings",
            headers=header,
            data=json.dumps(test_room_booking_payload),
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

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

        response_1 = test_app.delete(
            url="/rooms/" + str(room_id) + "/bookings/" + str(booking_1_id),
            headers=header
        )

        assert response_1.status_code == 200

        response_json_1 = response_1.json()

        # control that first rating is correct
        assert response_json_1["id"] == 1
        assert response_json_1["room_id"] == room_id
        assert response_json_1["date_to"] == test_room_booking_payload["date_to"]
        assert response_json_1["date_from"] == test_room_booking_payload["date_from"]

        _delete_room(test_app)
