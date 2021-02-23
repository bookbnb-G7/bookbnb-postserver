import json
import pytest

test_room_payload = {
    "id": 1,
    "title": "THE ROOM",
    "description": "You are tearing me apart Lisa",
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_uuid": 1,
    "longitude": 2,
    "latitude": 1,
    "location": "Canada",
    "price_per_day": 1800,
    "capacity": 7
}

test_another_room_payload = {
    "id": 2,
    "title": "THE ROOM 2",
    "description": "You are still tearing me apart Lisa",
    "type": "rancho",
    "owner": "pejelagarto",
    "owner_uuid": 2,
    "longitude": -46.3,
    "latitude": 51,
    "location": "USA",
    "price_per_day": 15,
    "capacity": 3
}

header = {"api-key": "ULTRAMEGAFAKEAPIKEY"}


def _create_room(test_app, payload):
    test_app.post(url="/rooms",
                  headers=header,
                  data=json.dumps(payload))


def _delete_room(test_app, room_id):
    test_app.delete(url="/rooms/" + str(room_id),
                    headers=header)


@pytest.mark.usefixtures("test_app")
class TestRoom:
    def test_get_recomended_rooms(self, test_app):
        # add rooms
        _create_room(test_app, test_room_payload)
        _create_room(test_app, test_another_room_payload)

        # get all rooms
        response = test_app.get("/recomendations",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()
        # control that room list metadata is correct
        assert response_json["amount"] == 2

        _delete_room(test_app, 1)
        _delete_room(test_app, 2)
