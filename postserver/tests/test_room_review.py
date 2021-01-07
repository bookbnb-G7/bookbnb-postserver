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
    "price_per_day": 1800.0,
    "capacity": 7,
}

test_room_review_payload = {
    "review": "copada",
    "reviewer": "facu, el crack",
    "reviewer_id": 1,
}

test_another_room_review_payload = {
    "review": "de otro world",
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
class TestRoomReview:
    def test_review_an_existing_room(self, test_app):
        _create_room(test_app)

        response = test_app.post(
            url="/rooms/" + str(room_id) + "/reviews/",
            headers=header,
            data=json.dumps(test_room_review_payload),
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["review"] == test_room_review_payload["review"]
        assert response_json["reviewer"] == test_room_review_payload["reviewer"]
        assert response_json["reviewer_id"] == test_room_review_payload["reviewer_id"]

    def test_review_a_room_without_api_key(self, test_app):
        response = test_app.post(
            url="/rooms/" + str(room_id) + "/reviews/",
            data=json.dumps(test_room_review_payload),
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_review_an_non_existent_room(self, test_app):
        not_existent_room_id = 25

        response = test_app.post(
            url="/rooms/" + str(not_existent_room_id) + "/reviews/",
            headers=header,
            data=json.dumps(test_room_review_payload),
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_an_existing_room_review(self, test_app):
        review_id = 1

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/reviews/" + str(review_id),
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["review"] == test_room_review_payload["review"]
        assert response_json["reviewer"] == test_room_review_payload["reviewer"]
        assert response_json["reviewer_id"] == test_room_review_payload["reviewer_id"]

    def test_get_an_non_existent_room_review(self, test_app):
        not_existent_room_review_id = 25

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/reviews/" + str(not_existent_room_review_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room review not found"

    def test_get_a_room_review_from_a_non_existen_room(self, test_app):
        review_id = 1
        not_existent_room_id = 25

        response = test_app.get(
            url="/rooms/" + str(not_existent_room_id) + "/reviews/" + str(review_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_all_existing_room_reviews_from_room(self, test_app):
        # add another room
        test_app.post(
            url="/rooms/" + str(room_id) + "/reviews/",
            headers=header,
            data=json.dumps(test_another_room_review_payload),
        )

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/reviews",
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        frt_review = response_json["reviews"][0]
        snd_review = response_json["reviews"][1]

        # control that first review is correct
        assert frt_review["id"] == 1
        assert frt_review["review"] == test_room_review_payload["review"]
        assert frt_review["reviewer"] == test_room_review_payload["reviewer"]
        assert frt_review["reviewer_id"] == test_room_review_payload["reviewer_id"]

        # control that second review is correct
        assert snd_review["id"] == 2
        assert snd_review["review"] == test_another_room_review_payload["review"]
        assert snd_review["reviewer"] == test_another_room_review_payload["reviewer"]
        assert snd_review["reviewer_id"] == test_another_room_review_payload["reviewer_id"]

        # controlas that review list metadata is correct
        assert response_json["amount"] == 2
        assert response_json["room_id"] == room_id

    def test_delete_a_non_existent_room_review(self, test_app):
        non_existent_room_review_id = 25

        response = test_app.delete(
            url="/rooms/" + str(room_id) + "/reviews/" + str(non_existent_room_review_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room review not found"

    def test_delete_a_room_review_from_a_non_existent_room(self, test_app):
        review_id = 1
        non_existent_room_id = 25

        response = test_app.delete(
            url="/rooms/" + str(non_existent_room_id) + "/reviews/" + str(review_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_delete_existing_room_reviews(self, test_app):
        review_1_id = 1
        review_2_id = 2

        response_1 = test_app.delete(
            url="/rooms/" + str(room_id) + "/reviews/" + str(review_1_id),
            headers=header
        )

        response_2 = test_app.delete(
            url="/rooms/" + str(room_id) + "/reviews/" + str(review_2_id),
            headers=header
        )

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        response_json_1 = response_1.json()
        response_json_2 = response_2.json()

        assert response_json_1["id"] == 1
        assert response_json_1["review"] == test_room_review_payload["review"]
        assert response_json_1["reviewer"] == test_room_review_payload["reviewer"]
        assert response_json_1["reviewer_id"] == test_room_review_payload["reviewer_id"]

        assert response_json_2["id"] == 2
        assert response_json_2["review"] == test_another_room_review_payload["review"]
        assert response_json_2["reviewer"] == test_another_room_review_payload["reviewer"]
        assert response_json_2["reviewer_id"] == test_another_room_review_payload["reviewer_id"]

        _delete_room(test_app)
