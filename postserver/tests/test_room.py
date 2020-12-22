import json
import pytest

test_room_payload = {
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_uuid": 1,
    "longitude": 2,
    "latitude": 1,
    "price_per_day": 1800.0,
    "capacity": 7
}

test_another_room_payload = {
    "type": "rancho",
    "owner": "pejelagarto",
    "owner_uuid": 2,
    "longitude": -46.3,
    "latitude": 51,
    "price_per_day": 15.0,
    "capacity": 3
}

test_room_booking_payload = {
    "user_id": 1,
    "date_ends": "2020-12-24",
    "date_begins": "2020-12-22",
    "amount_of_people": 3
}

test_another_room_booking_payload = {
    "user_id": 1,
    "date_ends": "2020-11-14",
    "date_begins": "2020-11-10",
    "amount_of_people": 3
}

header = {"api-key": "ULTRAMEGAFAKEAPIKEY"}


@pytest.mark.usefixtures("test_app")
class TestRoom:
    def test_create_room(self, test_app):
        response = test_app.post("/rooms/",
                                 headers=header,
                                 data=json.dumps(test_room_payload))

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["type"] == test_room_payload["type"]
        assert response_json["owner"] == test_room_payload["owner"]
        assert response_json["latitude"] == test_room_payload["latitude"]
        assert response_json["longitude"] == test_room_payload["longitude"]
        assert response_json["owner_uuid"] == test_room_payload["owner_uuid"]
        assert response_json["price_per_day"] == test_room_payload["price_per_day"]
        assert response_json["capacity"] == test_room_payload["capacity"]

    def test_create_room_without_api_key(self, test_app):
        response = test_app.post("/rooms/",
                                 data=json.dumps(test_room_payload))

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_get_existing_room(self, test_app):
        room_id = 1

        response = test_app.get("/rooms/" + str(room_id),
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["type"] == test_room_payload["type"]
        assert response_json["owner"] == test_room_payload["owner"]
        assert response_json["latitude"] == test_room_payload["latitude"]
        assert response_json["longitude"] == test_room_payload["longitude"]
        assert response_json["owner_uuid"] == test_room_payload["owner_uuid"]
        assert response_json["price_per_day"] == test_room_payload["price_per_day"]
        assert response_json["capacity"] == test_room_payload["capacity"]

    def test_get_non_existent_room(self, test_app):
        non_existent_room_id = 25

        response = test_app.get("/rooms/" + str(non_existent_room_id),
                                headers=header)

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_patch_existing_room(self, test_app):
        room_id = 1

        room_patch = {
            "latitude": 3.0,
            "longitude": 5.0,
            "type": "mansion",
            "price_per_day": 5000.0,
            "capacity": 6
        }

        response = test_app.patch("/rooms/" + str(room_id),
                                  data=json.dumps(room_patch),
                                  headers=header)

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["type"] == room_patch["type"]
        assert response_json["owner"] == test_room_payload["owner"]
        assert response_json["latitude"] == room_patch["latitude"]
        assert response_json["longitude"] == room_patch["longitude"]
        assert response_json["price_per_day"] == room_patch["price_per_day"]
        assert response_json["owner_uuid"] == test_room_payload["owner_uuid"]
        assert response_json["capacity"] == room_patch["capacity"]

        # after that we reset the changes

        room_reset_patch = {
            "type": test_room_payload["type"],
            "latitude": test_room_payload["latitude"],
            "longitude": test_room_payload["longitude"],
            "price_per_day": test_room_payload["price_per_day"],
            "capacity": test_room_payload["capacity"]
        }

        response = test_app.patch("/rooms/" + str(room_id),
                                  data=json.dumps(room_reset_patch),
                                  headers=header)

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["type"] == test_room_payload["type"]
        assert response_json["owner"] == test_room_payload["owner"]
        assert response_json["latitude"] == test_room_payload["latitude"]
        assert response_json["longitude"] == test_room_payload["longitude"]
        assert response_json["owner_uuid"] == test_room_payload["owner_uuid"]
        assert response_json["price_per_day"] == test_room_payload["price_per_day"]
        assert response_json["capacity"] == test_room_payload["capacity"]

    def test_patch_non_existent_room(self, test_app):
        non_existent_room_id = 25

        room_patch = {"type": "mansion", "price_per_day": 5000.0}

        response = test_app.patch("/rooms/" + str(non_existent_room_id),
                                  data=json.dumps(room_patch),
                                  headers=header)

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_all_existing_rooms(self, test_app):
        # add another room
        test_app.post("/rooms/",
                      data=json.dumps(test_another_room_payload),
                      headers=header)

        # get all rooms
        response = test_app.get("/rooms/",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        frt_room = response_json["rooms"][0]
        snd_room = response_json["rooms"][1]

        # control that first room is correct
        assert frt_room["id"] == 1
        assert frt_room["type"] == test_room_payload["type"]
        assert frt_room["owner"] == test_room_payload["owner"]
        assert frt_room["latitude"] == test_room_payload["latitude"]
        assert frt_room["longitude"] == test_room_payload["longitude"]
        assert frt_room["owner_uuid"] == test_room_payload["owner_uuid"]
        assert frt_room["price_per_day"] == test_room_payload["price_per_day"]
        assert frt_room["capacity"] == test_room_payload["capacity"]

        # control that second room is correct
        assert snd_room["id"] == 2
        assert snd_room["type"] == test_another_room_payload["type"]
        assert snd_room["owner"] == test_another_room_payload["owner"]
        assert snd_room["latitude"] == test_another_room_payload["latitude"]
        assert snd_room["longitude"] == test_another_room_payload["longitude"]
        assert snd_room["owner_uuid"] == test_another_room_payload["owner_uuid"]
        assert snd_room["price_per_day"] == test_another_room_payload["price_per_day"]
        assert snd_room["capacity"] == test_another_room_payload["capacity"]

        # control that room list metadata is correct
        assert response_json["amount"] == 2

    def test_get_all_existing_rooms_close_to_location(self, test_app):
        # To determine if a room is close to a given point, its coordinates must be
        # within a 0.1 distance from the given point

        # get all rooms close to (longitude: 2.01, latitude:1)
        response = test_app.get("/rooms/?longitude=2.01&latitude=1",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        frt_room = response_json["rooms"][0]

        # control that first room is correct
        assert frt_room["id"] == 1
        assert frt_room["type"] == test_room_payload["type"]
        assert frt_room["owner"] == test_room_payload["owner"]
        assert frt_room["latitude"] == test_room_payload["latitude"]
        assert frt_room["longitude"] == test_room_payload["longitude"]
        assert frt_room["owner_uuid"] == test_room_payload["owner_uuid"]
        assert frt_room["price_per_day"] == test_room_payload["price_per_day"]
        assert frt_room["capacity"] == test_room_payload["capacity"]

        # control that room list metadata is correct
        assert response_json["amount"] == 1


        # get all rooms close to (longitude: -46.31, latitude:51.02)
        response = test_app.get("/rooms/?longitude=-46.31&latitude=51.02",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        snd_room = response_json["rooms"][0]

        # control that second room is correct
        assert snd_room["id"] == 2
        assert snd_room["type"] == test_another_room_payload["type"]
        assert snd_room["owner"] == test_another_room_payload["owner"]
        assert snd_room["latitude"] == test_another_room_payload["latitude"]
        assert snd_room["longitude"] == test_another_room_payload["longitude"]
        assert snd_room["owner_uuid"] == test_another_room_payload["owner_uuid"]
        assert snd_room["price_per_day"] == test_another_room_payload["price_per_day"]
        assert snd_room["capacity"] == test_another_room_payload["capacity"]

        # control that room list metadata is correct
        assert response_json["amount"] == 1

        # get all rooms close to (longitude: 110, latitude:89.3)
        response = test_app.get("/rooms/?longitude=110&latitude=89.3",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        # control that room list metadata is correct
        assert response_json["amount"] == 0

    def test_get_all_existing_rooms_that_are_not_booked(self, test_app):
        room_id_1 = 1
        room_id_2 = 2

        # the first room is booked between 2020-12-22 to 2020-12-24
        test_app.post(
            url="/rooms/" + str(room_id_1) + "/bookings/",
            headers=header,
            data=json.dumps(test_room_booking_payload)
        )

        # the second room is booked between 2020-11-10 to 2020-11-14
        test_app.post(
            url="/rooms/" + str(room_id_2) + "/bookings/",
            headers=header,
            data=json.dumps(test_another_room_booking_payload)
        )

        # get all rooms not booked between (date_begins: 2020-11-3 and date_ends:2020-11-25)
        response = test_app.get("/rooms/?date_begins=2020-11-3&date_ends=2020-11-25",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        frt_room = response_json["rooms"][0]

        # control that first room is correct
        assert frt_room["id"] == 1
        assert frt_room["type"] == test_room_payload["type"]
        assert frt_room["owner"] == test_room_payload["owner"]
        assert frt_room["latitude"] == test_room_payload["latitude"]
        assert frt_room["longitude"] == test_room_payload["longitude"]
        assert frt_room["owner_uuid"] == test_room_payload["owner_uuid"]
        assert frt_room["price_per_day"] == test_room_payload["price_per_day"]
        assert frt_room["capacity"] == test_room_payload["capacity"]

        # control that room list metadata is correct
        assert response_json["amount"] == 1


        # get all rooms not booked between (date_begins: 2020-12-15 and date_ends:2020-12-25)
        response = test_app.get("/rooms/?date_begins=2020-12-15&date_ends=2020-12-25",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        snd_room = response_json["rooms"][0]

        # control that second room is correct
        assert snd_room["id"] == 2
        assert snd_room["type"] == test_another_room_payload["type"]
        assert snd_room["owner"] == test_another_room_payload["owner"]
        assert snd_room["latitude"] == test_another_room_payload["latitude"]
        assert snd_room["longitude"] == test_another_room_payload["longitude"]
        assert snd_room["owner_uuid"] == test_another_room_payload["owner_uuid"]
        assert snd_room["price_per_day"] == test_another_room_payload["price_per_day"]
        assert snd_room["capacity"] == test_another_room_payload["capacity"]

        # control that room list metadata is correct
        assert response_json["amount"] == 1

        # get all rooms not booked between (date_begins=2020-11-3 and date_ends=2020-12-30)
        response = test_app.get("/rooms/?date_begins=2020-11-3&date_ends=2020-12-30",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        # control that room list metadata is correct
        assert response_json["amount"] == 0

    def test_get_all_existing_rooms_that_have_enough_capacity(self, test_app):
        # To determine if a room is close to a given point, its coordinates must be
        # within a 0.1 distance from the given point

        # get all rooms that have a capacity for 4 persons or more
        response = test_app.get("/rooms/?people=4",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        # control that room list metadata is correct
        assert response_json["amount"] == 1

        frt_room = response_json["rooms"][0]

        # control that first room is correct
        assert frt_room["id"] == 1
        assert frt_room["type"] == test_room_payload["type"]
        assert frt_room["owner"] == test_room_payload["owner"]
        assert frt_room["latitude"] == test_room_payload["latitude"]
        assert frt_room["longitude"] == test_room_payload["longitude"]
        assert frt_room["owner_uuid"] == test_room_payload["owner_uuid"]
        assert frt_room["price_per_day"] == test_room_payload["price_per_day"]
        assert frt_room["capacity"] == test_room_payload["capacity"]


        # get all rooms that have a capacity for 1 person or more
        response = test_app.get("/rooms/?people=1",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        # control that room list metadata is correct
        assert response_json["amount"] == 2

        frt_room = response_json["rooms"][0]
        snd_room = response_json["rooms"][1]

        # control that first room is correct
        assert frt_room["id"] == 1
        assert frt_room["type"] == test_room_payload["type"]
        assert frt_room["owner"] == test_room_payload["owner"]
        assert frt_room["latitude"] == test_room_payload["latitude"]
        assert frt_room["longitude"] == test_room_payload["longitude"]
        assert frt_room["owner_uuid"] == test_room_payload["owner_uuid"]
        assert frt_room["price_per_day"] == test_room_payload["price_per_day"]
        assert frt_room["capacity"] == test_room_payload["capacity"]

        # control that second room is correct
        assert snd_room["id"] == 2
        assert snd_room["type"] == test_another_room_payload["type"]
        assert snd_room["owner"] == test_another_room_payload["owner"]
        assert snd_room["latitude"] == test_another_room_payload["latitude"]
        assert snd_room["longitude"] == test_another_room_payload["longitude"]
        assert snd_room["owner_uuid"] == test_another_room_payload["owner_uuid"]
        assert snd_room["price_per_day"] == test_another_room_payload["price_per_day"]
        assert snd_room["capacity"] == test_another_room_payload["capacity"]

        # get all rooms that have a capacity for 11 persons or more
        response = test_app.get("/rooms/?people=11",
                                headers=header)

        assert response.status_code == 200

        response_json = response.json()

        # control that room list metadata is correct
        assert response_json["amount"] == 0

    def test_delete_existing_room(self, test_app):
        room_1_id = 1
        room_2_id = 2

        response_1 = test_app.delete("/rooms/" + str(room_1_id), headers=header)
        response_2 = test_app.delete("/rooms/" + str(room_2_id), headers=header)

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        response_json_1 = response_1.json()
        response_json_2 = response_2.json()

        assert response_json_1["id"] == room_1_id
        assert response_json_1["type"] == test_room_payload["type"]
        assert response_json_1["owner"] == test_room_payload["owner"]
        assert response_json_1["latitude"] == test_room_payload["latitude"]
        assert response_json_1["longitude"] == test_room_payload["longitude"]
        assert response_json_1["owner_uuid"] == test_room_payload["owner_uuid"]
        assert response_json_1["price_per_day"] == test_room_payload["price_per_day"]
        assert response_json_1["capacity"] == test_room_payload["capacity"]

        assert response_json_2["id"] == room_2_id
        assert response_json_2["type"] == test_another_room_payload["type"]
        assert response_json_2["owner"] == test_another_room_payload["owner"]
        assert response_json_2["latitude"] == test_another_room_payload["latitude"]
        assert response_json_2["longitude"] == test_another_room_payload["longitude"]
        assert response_json_2["owner_uuid"] == test_another_room_payload["owner_uuid"]
        assert response_json_2["price_per_day"] == test_another_room_payload["price_per_day"]
        assert response_json_2["capacity"] == test_another_room_payload["capacity"]

    def test_delete_not_existent_room(self, test_app):
        non_existent_room_id = 25

        response = test_app.delete("/rooms/" + str(non_existent_room_id),
                                   headers=header)

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"
