import json

def test_create_room(test_app):
    test_request_payload = {
        'type': 'traphouse', 
        'owner': 'facu, el crack',
        'owner_id': 1,
        'price_per_day': 1800.0
    }
    
    expected_response = {
        'id': 1,
        'type': 'traphouse', 
        'owner': 'facu, el crack',
        'owner_id': 1,
        'price_per_day': 1800.0
    }

    response = test_app.post(
        '/rooms/',
        data = json.dumps(test_request_payload)
    )

    print(response)

    assert response.status_code == 201
    assert response.json() == expected_response


def test_rate_existing_room(test_app):
    room_id = 1 

    test_request_payload = {
        'rating': 3,
        'reviewer': "facu",
        'reviewer_id': 1
    }

    expected_response = {
        'id': 1,
        'room_id': room_id,
        'rating': 3,
        'reviewer': "facu",
        'reviewer_id': 1
    }    

    response = test_app.post(
        '/rooms/' + str(room_id) + '/ratings',
        data = json.dumps(test_request_payload)
    )

    assert response.status_code == 201
    assert response.json() == expected_response


def test_review_existing_room(test_app):
    room_id = 1 

    test_request_payload = {
        'review': 'buenarda',
        'reviewer': "facu",
        'reviewer_id': 1
    }

    expected_response = {
        'id': 1,
        'room_id': room_id,
        'review': 'buenarda',
        'reviewer': "facu",
        'reviewer_id': 1
    }    

    response = test_app.post(
        '/rooms/' + str(room_id) + '/reviews',
        data = json.dumps(test_request_payload)
    )

    assert response.status_code == 201
    assert response.json() == expected_response


def test_get_existing_room(test_app):
    room_id = 1

    expected_response = {
        'id': room_id,
        'type': 'traphouse', 
        'owner': 'facu, el crack',
        'owner_id': 1,
        'price_per_day': 1800.0
    }

    response = test_app.get(
        '/rooms/' + str(room_id),
    )

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_existing_review_by_id(test_app):
    room_id = 1
    review_id = 1

    expected_response = {
        'id': review_id,
        'room_id': room_id,
        'review': 'buenarda',
        'reviewer': "facu",
        'reviewer_id': 1
    }    

    response = test_app.get(
        '/rooms/' + str(room_id) + '/reviews/' + str(review_id),
    )

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_existing_rating_by_id(test_app):
    room_id = 1
    rating_id = 1

    expected_response = {
        'id': rating_id,
        'room_id': room_id,
        'rating': 3,
        'reviewer': "facu",
        'reviewer_id': 1
    }    

    response = test_app.get(
        '/rooms/' + str(room_id) + '/ratings/' + str(rating_id),
    )

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_all_room_ratings(test_app):
    room_id = 1
    
    expected_response = {
        'ratings': [{
            'id': 1,
            'room_id': room_id,
            'rating': 3,
            'reviewer': "facu",
            'reviewer_id': 1
        }],
        'room_id': room_id
    }


    response = test_app.get(
        '/rooms/' + str(room_id) + '/ratings',
    )

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_all_room_reviews(test_app):
    room_id = 1
    
    expected_response = {
        'reviews': [{
            'id': 1,
            'room_id': room_id,
            'review': 'buenarda',
            'reviewer': "facu",
            'reviewer_id': 1
        }],
        'room_id': room_id
    }


    response = test_app.get(
        '/rooms/' + str(room_id) + '/reviews',
    )

    assert response.status_code == 200
    assert response.json() == expected_response
