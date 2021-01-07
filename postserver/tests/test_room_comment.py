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
    "price_per_day": 1800.0,
    "capacity": 7,
}

test_room_comment_payload = {
    "comment": "copada",
    "commentator": "no soy facu",
    "commentator_id": 2,
}

test_another_room_comment_payload = {
    "comment": "tremendous",
    "commentator": "no soy facu",
    "commentator_id": 3,
    "main_comment_id": 1,

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
class TestRoomComment:
    def test_comment_an_existing_room(self, test_app):
        _create_room(test_app)

        response = test_app.post(
            url="/rooms/" + str(room_id) + "/comments",
            headers=header,
            data=json.dumps(test_room_comment_payload),
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["comment"] == test_room_comment_payload["comment"]
        assert response_json["commentator"] == test_room_comment_payload["commentator"]
        assert response_json["commentator_id"] == test_room_comment_payload["commentator_id"]

    def test_comment_a_room_without_api_key(self, test_app):
        response = test_app.post(
            url="/rooms/" + str(room_id) + "/comments",
            data=json.dumps(test_room_comment_payload),
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json["error"] == "Revoked API key"

    def test_comment_an_non_existent_room(self, test_app):
        not_existent_room_id = 25

        response = test_app.post(
            url="/rooms/" + str(not_existent_room_id) + "/comments",
            headers=header,
            data=json.dumps(test_room_comment_payload),
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_an_existing_room_comment(self, test_app):
        comment_id = 1

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/comments/" + str(comment_id),
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json["id"] == 1
        assert response_json["comment"] == test_room_comment_payload["comment"]
        assert response_json["commentator"] == test_room_comment_payload["commentator"]
        assert response_json["commentator_id"] == test_room_comment_payload["commentator_id"]

    def test_get_an_non_existent_room_comment(self, test_app):
        not_existent_room_comment_id = 25

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/comments/" + str(not_existent_room_comment_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room comment not found"

    def test_get_a_room_comment_from_a_non_existen_room(self, test_app):
        comment_id = 1
        not_existent_room_id = 25

        response = test_app.get(
            url="/rooms/" + str(not_existent_room_id) + "/comments/" + str(comment_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_get_all_existing_room_comments_from_room(self, test_app):
        # add another room comment, this is an answer to the first one
        test_app.post(
            url="/rooms/" + str(room_id) + "/comments",
            headers=header,
            data=json.dumps(test_another_room_comment_payload),
        )

        response = test_app.get(
            url="/rooms/" + str(room_id) + "/comments",
            headers=header
        )

        assert response.status_code == 200

        response_json = response.json()

        # check that review list metadata is correct
        assert response_json["amount"] == 2
        assert response_json["room_id"] == room_id

        frt_review = response_json["comments"][0]["comment"]
        snd_review = response_json["comments"][0]["answers"][0]

        # control that first comment is correct
        assert frt_review["id"] == 1
        assert frt_review["comment"] == test_room_comment_payload["comment"]
        assert frt_review["commentator"] == test_room_comment_payload["commentator"]
        assert frt_review["commentator_id"] == test_room_comment_payload["commentator_id"]

        # control that second comment is correct
        assert snd_review["id"] == 2
        assert snd_review["comment"] == test_another_room_comment_payload["comment"]
        assert snd_review["commentator"] == test_another_room_comment_payload["commentator"]
        assert snd_review["commentator_id"] == test_another_room_comment_payload["commentator_id"]
        assert snd_review["main_comment_id"] == test_another_room_comment_payload["main_comment_id"]

    def test_delete_a_non_existent_room_comment(self, test_app):
        non_existent_room_comment_id = 25

        response = test_app.delete(
            url="/rooms/" + str(room_id) + "/comments/" + str(non_existent_room_comment_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room comment not found"

    def test_delete_a_room_comment_from_a_non_existent_room(self, test_app):
        comment_id = 1
        non_existent_room_id = 25

        response = test_app.delete(
            url="/rooms/" + str(non_existent_room_id) + "/comments/" + str(comment_id),
            headers=header
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["error"] == "room not found"

    def test_delete_existing_room_comments(self, test_app):
        # Deleting a main comment should delete also its answers

        comment_1_id = 1
        comment_2_id = 2

        response_1 = test_app.delete(
            url="/rooms/" + str(room_id) + "/comments/" + str(comment_1_id),
            headers=header
        )

        assert response_1.status_code == 200

        response_json_1 = response_1.json()

        assert response_json_1["id"] == 1
        assert response_json_1["comment"] == test_room_comment_payload["comment"]
        assert response_json_1["commentator"] == test_room_comment_payload["commentator"]
        assert response_json_1["commentator_id"] == test_room_comment_payload["commentator_id"]

        response_2 = test_app.delete(
            url="/rooms/" + str(room_id) + "/comments/" + str(comment_2_id),
            headers=header
        )

        assert response_2.status_code == 404

        response_json_2 = response_2.json()

        assert response_json_2["error"] == "room comment not found"

        _delete_room(test_app)
