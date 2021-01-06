import json
import pytest

room_id = 1

test_room_payload = {
    "id": 1,
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_uuid": 1,
    "latitude": 1.0,
    "longitude": 2.0,
    "location": "USA",
    "price_per_day": 1000.0,
    "capacity": 7,
}

test_room_rating_payload = {
    "rating": 10.0,
    "reviewer": "facu, el crack",
    "reviewer_id": 1,
}

test_another_room_rating_payload = {
    "rating": 5.0,
    "reviewer": "facu, pero otro",
    "reviewer_id": 2,
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
class TestRoomRating:
    def test_rate_an_existing_room(self, test_app):
        _create_room(test_app)

        response = test_app.post(
            url="/rooms/" + str(room_id) + "/ratings/",
            headers=header,
            data=json.dumps(test_room_rating_payload),
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["rating"] == test_room_rating_payload["rating"]
        assert response_json["reviewer"] == test_room_rating_payload["reviewer"]
        assert response_json["reviewer_id"] == test_room_rating_payload["reviewer_id"]

    def test_rate_a_room_without_api_key(self, test_app):
        response = test_app.post(
            url="/rooms/" + str(room_id) + "/ratings/",
            data=json.dumps(test_room_rating_payload),
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_rate_an_non_existent_room(self, test_app):
        not_existent_room_id = 25

        response = test_app.post(
            url="/rooms/" + str(not_existent_room_id) + "/ratings/",
            headers=header,
            data=json.dumps(test_room_rating_payload),
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_an_existing_room_rating(self, test_app):
        rating_id = 1

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/ratings/" + str(rating_id),
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["rating"] == test_room_rating_payload["rating"]
        assert response_json["reviewer"] == test_room_rating_payload["reviewer"]
        assert response_json["reviewer_id"] == test_room_rating_payload["reviewer_id"]

    def test_get_an_non_existent_room_rating(self, test_app):
        not_existent_room_rating_id = 25

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/ratings/" + str(not_existent_room_rating_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room rating not found"

    def test_get_a_room_rating_from_a_non_existen_room(self, test_app):
        rating_id = 1
        not_existent_room_id = 25

        response = test_app.get(
            url="/rooms/" + str(not_existent_room_id) + "/ratings/" + str(rating_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_all_existing_room_ratings_from_room(self, test_app):
        # add another rating to the existing room
        test_app.post(
            url="/rooms/" + str(room_id) + "/ratings/",
            headers=header,
            data=json.dumps(test_another_room_rating_payload)
        )

        # get all ratings

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/ratings",
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        frt_rating = response_json["ratings"][0]
        snd_rating = response_json["ratings"][1]

        # control that first rating is correct
        assert frt_rating["id"] == 1
        assert frt_rating["rating"] == test_room_rating_payload["rating"]
        assert frt_rating["reviewer"] == test_room_rating_payload["reviewer"]
        assert frt_rating["reviewer_id"] == test_room_rating_payload["reviewer_id"]

        # control that second rating is correct
        assert snd_rating["id"] == 2
        assert snd_rating["rating"] == test_another_room_rating_payload["rating"]
        assert snd_rating["reviewer"] == test_another_room_rating_payload["reviewer"]
        assert snd_rating["reviewer_id"] == test_another_room_rating_payload["reviewer_id"]

        # controlas that rating list metadata is correct
        assert response_json["amount"] == 2
        assert response_json["room_id"] == room_id

    def test_delete_a_non_existent_room_rating(self, test_app):
        non_existent_room_rating_id = 25

        response = test_app.delete(
            url="/rooms/" + str(room_id) + "/ratings/" + str(non_existent_room_rating_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room rating not found"

    def test_delete_a_room_rating_from_a_non_existent_room(self, test_app):
        rating_id = 1
        non_existent_room_id = 25

        response = test_app.delete(
            url="/rooms/" + str(non_existent_room_id) + "/ratings/" + str(rating_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_delete_existing_room_ratings(self, test_app):
        rating_1_id = 1
        rating_2_id = 2

        response_1 = test_app.delete(
            url="/rooms/" + str(room_id) + "/ratings/" + str(rating_1_id),
            headers=header
        )

        response_2 = test_app.delete(
            url="/rooms/" + str(room_id) + "/ratings/" + str(rating_2_id),
            headers=header
        )

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        response_json_1 = response_1.json()
        response_json_2 = response_2.json()

        assert response_json_1["id"] == 1
        assert response_json_1["rating"] == test_room_rating_payload["rating"]
        assert response_json_1["reviewer"] == test_room_rating_payload["reviewer"]
        assert response_json_1["reviewer_id"] == test_room_rating_payload["reviewer_id"]

        assert response_json_2["id"] == 2
        assert response_json_2["rating"] == test_another_room_rating_payload["rating"]
        assert response_json_2["reviewer"] == test_another_room_rating_payload["reviewer"]
        assert response_json_2["reviewer_id"] == test_another_room_rating_payload["reviewer_id"]

        _delete_room(test_app)
