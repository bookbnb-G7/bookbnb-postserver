import json

test_room_payload = {
    "type": "traphouse",
    "owner": "facu, el crack",
    "owner_id": 1,
    "price_per_day": 1800.0,
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

room_id = 1

"""
def _create_room(test_app):
    test_app.post("/rooms/", data=json.dumps(test_room_payload))


def _delete_room(test_app):
    test_app.delete("/rooms/" + str(room_id))


def test_review_an_existing_room(test_app):
    _create_room(test_app)

    response = test_app.post(
        "/rooms/" + str(room_id) + "/reviews/",
        data=json.dumps(test_room_review_payload),
    )

    assert response.status_code == 201

    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["review"] == test_room_review_payload["review"]
    assert response_json["reviewer"] == test_room_review_payload["reviewer"]
    assert response_json["reviewer_id"] == test_room_review_payload["reviewer_id"]


def test_review_an_non_existent_room(test_app):
    not_existent_room_id = 25

    response = test_app.post(
        "/rooms/" + str(not_existent_room_id) + "/reviews/",
        data=json.dumps(test_room_review_payload),
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room not found"


def test_get_an_existing_room_review(test_app):
    review_id = 1

    response = test_app.get(
        "/rooms/" + str(room_id) + "/reviews/" + str(review_id),
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["review"] == test_room_review_payload["review"]
    assert response_json["reviewer"] == test_room_review_payload["reviewer"]
    assert response_json["reviewer_id"] == test_room_review_payload["reviewer_id"]


def test_get_an_non_existent_room_review(test_app):
    not_existent_room_review_id = 25

    response = test_app.get(
        "/rooms/" + str(room_id) + "/reviews/" + str(not_existent_room_review_id),
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room review not found"


def test_get_a_room_review_from_a_non_existen_room(test_app):
    review_id = 1
    not_existent_room_id = 25

    response = test_app.get(
        "/rooms/" + str(not_existent_room_id) + "/reviews/" + str(review_id),
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room not found"


def test_patch_an_existing_room_review(test_app):
    review_id = 1

    room_review_patch = {"review": "ya no tan copada"}

    response = test_app.patch(
        "/rooms/" + str(room_id) + "/reviews/" + str(review_id),
        data=json.dumps(room_review_patch),
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["review"] == room_review_patch["review"]
    assert response_json["reviewer"] == test_room_review_payload["reviewer"]
    assert response_json["reviewer_id"] == test_room_review_payload["reviewer_id"]

    # reset changes}

    room_review_reset_patch = {"review": test_room_review_payload["review"]}

    response = test_app.patch(
        "/rooms/" + str(room_id) + "/reviews/" + str(review_id),
        data=json.dumps(room_review_reset_patch),
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["review"] == test_room_review_payload["review"]
    assert response_json["reviewer"] == test_room_review_payload["reviewer"]
    assert response_json["reviewer_id"] == test_room_review_payload["reviewer_id"]


def test_patch_a_non_existent_room_review(test_app):
    not_existent_room_review_id = 25

    room_review_patch = {"review": "buernarda"}

    response = test_app.patch(
        "/rooms/" + str(room_id) + "/reviews/" + str(not_existent_room_review_id),
        data=json.dumps(room_review_patch),
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room review not found"


def test_patch_a_room_review_from_a_not_existing_room(test_app):
    room_review_id = 1
    non_existent_room_id = 25

    room_review_patch = {"review": "buernarda"}

    response = test_app.patch(
        "/rooms/" + str(non_existent_room_id) + "/reviews/" + str(room_review_id),
        data=json.dumps(room_review_patch),
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room not found"


def test_get_all_existing_room_reviews_from_room(test_app):
    # add another review to the existing room

    response = test_app.post(
        "/rooms/" + str(room_id) + "/reviews/",
        data=json.dumps(test_another_room_review_payload),
    )

    # get all reviews

    response = test_app.get(
        "/rooms/" + str(room_id) + "/reviews",
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


def test_delete_a_non_existent_room_review(test_app):
    non_existent_room_review_id = 25

    response = test_app.delete(
        "/rooms/" + str(room_id) + "/reviews/" + str(non_existent_room_review_id)
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room review not found"


def test_delete_a_room_review_from_a_non_existent_room(test_app):
    review_id = 1
    non_existent_room_id = 25

    response = test_app.delete(
        "/rooms/" + str(non_existent_room_id) + "/reviews/" + str(review_id)
    )

    assert response.status_code == 404

    response_json = response.json()

    assert response_json["error"] == "room not found"


def test_delete_existing_room_reviews(test_app):
    review_1_id = 1
    review_2_id = 2

    response_1 = test_app.delete(
        "/rooms/" + str(room_id) + "/reviews/" + str(review_1_id),
    )

    response_2 = test_app.delete(
        "/rooms/" + str(room_id) + "/reviews/" + str(review_2_id),
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
    assert (
        response_json_2["reviewer_id"]
        == test_another_room_review_payload["reviewer_id"]
    )
"""