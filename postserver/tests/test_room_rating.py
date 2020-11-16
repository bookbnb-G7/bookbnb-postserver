import json
import pytest

test_room_payload = {
    'type': 'traphouse', 
    'owner': 'facu, el crack',
    'owner_id': 1,
    'price_per_day': 1800.0
}

test_room_rating_payload = {
    'rating': 10.0, 
    'reviewer': 'facu, el crack',
    'reviewer_id': 1
}

test_another_room_rating_payload = {
    'rating': 5.0, 
    'reviewer': 'facu, pero otro',
    'reviewer_id': 2
}

room_id = 1


def _create_room(test_app):
    test_app.post(
        '/rooms/',
        data = json.dumps(test_room_payload)
    )

def _delete_room(test_app):
    test_app.delete(
        '/rooms/' + str(room_id)
    )


def test_rate_an_existing_room(test_app):   
    _create_room(test_app)

    response = test_app.post(
        '/rooms/' + str(room_id) + '/ratings/',
        data = json.dumps(test_room_rating_payload)
    )

    assert response.status_code == 201

    response_json = response.json()
    
    assert response_json['id'] == 1 
    assert response_json['rating'] == test_room_rating_payload['rating']
    assert response_json['reviewer'] == test_room_rating_payload['reviewer']
    assert response_json['reviewer_id'] == test_room_rating_payload['reviewer_id']


def test_rate_an_non_existent_room(test_app):   
    not_existent_room_id = 25

    response = test_app.post(
        '/rooms/' + str(not_existent_room_id) + '/ratings/',
        data = json.dumps(test_room_rating_payload)
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room not found' 


def test_get_an_existing_room_rating(test_app):
    rating_id = 1

    response = test_app.get(
        '/rooms/' + str(room_id) + '/ratings/' + str(rating_id),
    )

    assert response.status_code == 200

    response_json = response.json()
    
    assert response_json['id'] == 1 
    assert response_json['rating'] == test_room_rating_payload['rating']
    assert response_json['reviewer'] == test_room_rating_payload['reviewer']
    assert response_json['reviewer_id'] == test_room_rating_payload['reviewer_id']


def test_get_an_non_existent_room_rating(test_app):   
    not_existent_room_rating_id = 25

    response = test_app.get(
        '/rooms/' + str(room_id) + '/ratings/' + str(not_existent_room_rating_id),
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room rating not found' 


def test_get_a_room_rating_from_a_non_existen_room(test_app):   
    rating_id = 1
    not_existent_room_id = 25

    response = test_app.get(
        '/rooms/' + str(not_existent_room_id) + '/ratings/' + str(rating_id),
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room not found' 


def test_patch_an_existing_room_rating(test_app):
    rating_id = 1

    room_rating_patch = {
        'rating': 0
    }

    response = test_app.patch(
        '/rooms/' + str(room_id) + '/ratings/' + str(rating_id),
        data = json.dumps(room_rating_patch)
    )

    assert response.status_code == 200

    response_json = response.json()
    
    assert response_json['id'] == 1 
    assert response_json['rating'] == room_rating_patch['rating']
    assert response_json['reviewer'] == test_room_rating_payload['reviewer']
    assert response_json['reviewer_id'] == test_room_rating_payload['reviewer_id']

    # reset changes}

    room_rating_reset_patch = {
        'rating': test_room_rating_payload['rating']
    }

    response = test_app.patch(
        '/rooms/' + str(room_id) + '/ratings/' + str(rating_id),
        data = json.dumps(room_rating_reset_patch)
    )

    assert response.status_code == 200

    response_json = response.json()
    
    assert response_json['id'] == 1 
    assert response_json['rating'] == test_room_rating_payload['rating']
    assert response_json['reviewer'] == test_room_rating_payload['reviewer']
    assert response_json['reviewer_id'] == test_room_rating_payload['reviewer_id']


def test_patch_a_non_existent_room_rating(test_app):   
    not_existent_room_rating_id = 25

    room_rating_patch = {
        'rating': 0
    }

    response = test_app.patch(
        '/rooms/' + str(room_id) + '/ratings/' + str(not_existent_room_rating_id),
        data = json.dumps(room_rating_patch)
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room rating not found' 


def test_patch_a_room_rating_from_a_not_existing_room(test_app):   
    room_rating_id = 1
    non_existent_room_id = 25

    room_rating_patch = {
        'rating': 0
    }

    response = test_app.patch(
        '/rooms/' + str(non_existent_room_id) + '/ratings/' + str(room_rating_id),
        data = json.dumps(room_rating_patch)
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room not found' 


def test_get_all_existing_room_ratings_from_room(test_app):
    rating_1_id = 1

    # add another rating to the existing room
    
    response = test_app.post(
        '/rooms/' + str(room_id) + '/ratings/',
        data = json.dumps(test_another_room_rating_payload)
    )

    rating_2_id = response.json()['id']

    # get all ratings

    response = test_app.get(
        '/rooms/' + str(room_id) + '/ratings',
    )

    assert response.status_code == 200

    response_json = response.json()
    
    frt_rating = response_json['ratings'][0]
    snd_rating = response_json['ratings'][1] 

    # control that first rating is correct
    assert frt_rating['id'] == 1 
    assert frt_rating['rating'] == test_room_rating_payload['rating']
    assert frt_rating['reviewer'] == test_room_rating_payload['reviewer']
    assert frt_rating['reviewer_id'] == test_room_rating_payload['reviewer_id']

    # control that second rating is correct
    assert snd_rating['id'] == 2
    assert snd_rating['rating'] == test_another_room_rating_payload['rating']
    assert snd_rating['reviewer'] == test_another_room_rating_payload['reviewer']
    assert snd_rating['reviewer_id'] == test_another_room_rating_payload['reviewer_id']

    # controlas that rating list metadata is correct
    assert response_json['amount'] == 2
    assert response_json['room_id'] == room_id


def test_delete_a_non_existent_room_rating(test_app):   
    non_existent_room_rating_id = 25

    response = test_app.delete(
        '/rooms/' + str(room_id) + '/ratings/' + str(non_existent_room_rating_id)
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room rating not found' 


def test_delete_a_room_rating_from_a_non_existent_room(test_app):   
    rating_id = 1
    non_existent_room_id = 25

    response = test_app.delete(
        '/rooms/' + str(non_existent_room_id) + '/ratings/' + str(rating_id)
    )

    assert response.status_code == 404

    response_json = response.json()
    
    assert response_json['error'] == 'room not found' 


def test_delete_existing_room_ratings(test_app):
    rating_1_id = 1
    rating_2_id = 2

    response_1 = test_app.delete(
        '/rooms/' + str(room_id) + '/ratings/' + str(rating_1_id),
    )

    response_2 = test_app.delete(
        '/rooms/' + str(room_id) + '/ratings/' + str(rating_2_id),
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    response_json_1 = response_1.json()
    response_json_2 = response_2.json()    

    assert response_json_1['id'] == 1 
    assert response_json_1['rating'] == test_room_rating_payload['rating']
    assert response_json_1['reviewer'] == test_room_rating_payload['reviewer']
    assert response_json_1['reviewer_id'] == test_room_rating_payload['reviewer_id']

    assert response_json_2['id'] == 2
    assert response_json_2['rating'] == test_another_room_rating_payload['rating']
    assert response_json_2['reviewer'] == test_another_room_rating_payload['reviewer']
    assert response_json_2['reviewer_id'] == test_another_room_rating_payload['reviewer_id']

    _delete_room(test_app)

