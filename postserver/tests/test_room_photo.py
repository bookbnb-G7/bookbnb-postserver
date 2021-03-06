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
    "location": "USA",
    "price_per_day": 1000.0,
    "capacity": 7,
}


test_room_photo_payload = {
    "url": "www.queganasdesalirdejoda.com",
    "firebase_id": 1
}

test_another_room_photo_payload = {
    "url": "www.sigoconganasdesalirdejoda.com",
    "firebase_id": 2,
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
class TestRoomPhoto:
    def test_upload_photo_for_existing_room(self, test_app):
        _create_room(test_app)

        response = test_app.post(
            url="/rooms/" + str(room_id) + "/photos",
            headers=header,
            data=json.dumps(test_room_photo_payload)
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["url"] == test_room_photo_payload["url"]
        assert response_json["firebase_id"] == test_room_photo_payload["firebase_id"]

    def test_upload_photo_without_api_key(self, test_app):
        response = test_app.post(
            url="/rooms/" + str(room_id) + "/photos",
            data=json.dumps(test_room_photo_payload)
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_get_existing_photo_from_room(self, test_app):
        firebase_id = test_room_photo_payload["firebase_id"]

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/photos/" + str(firebase_id),
            headers=header)

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["url"] == test_room_photo_payload["url"]
        assert response_json["firebase_id"] == test_room_photo_payload["firebase_id"]

    def test_get_all_photos_from_room(self, test_app):
        test_app.post(
            url="/rooms/" + str(room_id) + "/photos",
            headers=header,
            data=json.dumps(test_another_room_photo_payload),
        )

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/photos",
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        frt_photo = response_json["room_photos"][0]
        snd_photo = response_json["room_photos"][1]

        # control that first photo is correct
        assert frt_photo["id"] == 1
        assert frt_photo["url"] == test_room_photo_payload["url"]
        assert frt_photo["firebase_id"] == test_room_photo_payload["firebase_id"]

        # control that first photo is correct
        assert snd_photo["id"] == 2
        assert snd_photo["url"] == test_another_room_photo_payload["url"]
        assert snd_photo["firebase_id"] == test_another_room_photo_payload["firebase_id"]

        # controlas that review list metadata is correct
        assert response_json["amount"] == 2
        assert response_json["room_id"] == room_id

    def test_delete_existing_room_photos(self, test_app):
        room_photo_1_id = 1
        room_photo_2_id = 2

        response_1 = test_app.delete(
            url="/rooms/" + str(room_id) + "/photos/" + str(room_photo_1_id),
            headers=header
        )

        response_2 = test_app.delete(
            url="/rooms/" + str(room_id) + "/photos/" + str(room_photo_2_id),
            headers=header
        )

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        response_json_1 = response_1.json()
        response_json_2 = response_2.json()

        assert response_json_1["id"] == 1
        assert response_json_1["url"] == test_room_photo_payload["url"]
        assert response_json_1["firebase_id"] == test_room_photo_payload["firebase_id"]

        assert response_json_2["id"] == 2
        assert response_json_2["url"] == test_another_room_photo_payload["url"]
        assert (
                response_json_2["firebase_id"] == test_another_room_photo_payload["firebase_id"]
        )

        _delete_room(test_app)
