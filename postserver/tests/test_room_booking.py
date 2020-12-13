import json
import datetime

room_id = 1

test_room_payload = {
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_uuid": 1,
    "price_per_day": 1000.0,
}

test_room_booking_payload = {
    "user_id": 1,
    "date_ends": "2020-12-30",
    "date_begins": "2020-12-15",
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


def test_book_an_existing_room(test_app):
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


def test_get_an_existing_room_booking(test_app):
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

    _delete_room(test_app)