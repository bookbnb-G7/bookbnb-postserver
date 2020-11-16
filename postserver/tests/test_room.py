import json

test_room_payload = {
    'type': 'traphouse', 
    'owner': 'facu, el crack',
    'owner_id': 1,
    'price_per_day': 1800.0
}
    
test_another_room_payload = {
    'type': 'rancho',
    'owner': 'pejelagarto',
    'owner_id': 2,
    'price_per_day': 15.0
}


def test_create_room(test_app):
    response = test_app.post(
        '/rooms/',
        data = json.dumps(test_room_payload)
    )

    print(response)

    assert response.status_code == 201

    response_json = response.json()
    
    assert response_json['id'] == 1 
    assert response_json['type'] == test_room_payload['type']
    assert response_json['owner'] == test_room_payload['owner']
    assert response_json['owner_id'] == test_room_payload['owner_id']
    assert response_json['price_per_day'] == test_room_payload['price_per_day']


def test_get_existing_room(test_app):
    room_id = 1

    response = test_app.get(
        '/rooms/' + str(room_id)
    )

    assert response.status_code == 200

    response_json = response.json() 

    assert response_json['id'] == 1 
    assert response_json['type'] == test_room_payload['type']
    assert response_json['owner'] == test_room_payload['owner']
    assert response_json['owner_id'] == test_room_payload['owner_id']
    assert response_json['price_per_day'] == test_room_payload['price_per_day']


def test_get_non_existent_room(test_app):
    non_existent_room_id = 25

    response = test_app.get(
        '/rooms/' + str(non_existent_room_id)
    )

    assert response.status_code == 404

    response_json = response.json() 

    assert response_json['error'] == 'not found'


def test_patch_existing_room(test_app):
    room_id = 1

    room_patch = {
        'type': 'mansion', 
        'price_per_day': 5000.0
    }

    response = test_app.patch(
        '/rooms/' + str(room_id),
        data = json.dumps(room_patch)
    )

    assert response.status_code == 200

    response_json = response.json() 

    assert response_json['id'] == 1 
    assert response_json['type'] == room_patch['type']
    assert response_json['owner'] == test_room_payload['owner']
    assert response_json['owner_id'] == test_room_payload['owner_id']
    assert response_json['price_per_day'] == room_patch['price_per_day']

    # after that we reset the changes

    room_reset_patch = {
        'type': test_room_payload['type'],
        'price_per_day': test_room_payload['price_per_day']
    }

    response = test_app.patch(
        '/rooms/' + str(room_id),
        data = json.dumps(room_reset_patch)
    )

    assert response.status_code == 200

    response_json = response.json() 

    assert response_json['id'] == 1 
    assert response_json['type'] == test_room_payload['type']
    assert response_json['owner'] == test_room_payload['owner']
    assert response_json['owner_id'] == test_room_payload['owner_id']
    assert response_json['price_per_day'] == test_room_payload['price_per_day']


def test_patch_non_existent_room(test_app):
    non_existent_room_id = 25

    room_patch = {
        'type': 'mansion', 
        'price_per_day': 5000.0
    }

    response = test_app.patch(
        '/rooms/' + str(non_existent_room_id),
        data = json.dumps(room_patch)
    )

    assert response.status_code == 404

    response_json = response.json() 

    assert response_json['error'] == 'not found'


def test_get_all_existing_room_ratings_from_room(test_app):
    rating_1_id = 1

    # add another room
    
    response = test_app.post(
        '/rooms/',
        data = json.dumps(test_another_room_payload)
    )

    room_2_id = 2

    # get all ratings

    response = test_app.get(
        '/rooms/',
    )

    assert response.status_code == 200

    response_json = response.json()
    
    frt_room = response_json['rooms'][0]
    snd_room = response_json['rooms'][1] 

    # control that first rating is correct
    assert frt_room['id'] == 1 
    assert frt_room['type'] == test_room_payload['type']
    assert frt_room['owner'] == test_room_payload['owner']
    assert frt_room['owner_id'] == test_room_payload['owner_id']
    assert frt_room['price_per_day'] == test_room_payload['price_per_day']

    # control that second rating is correct
    assert snd_room['id'] == 2
    assert snd_room['type'] == test_another_room_payload['type']
    assert snd_room['owner'] == test_another_room_payload['owner']
    assert snd_room['owner_id'] == test_another_room_payload['owner_id']
    assert snd_room['price_per_day'] == test_another_room_payload['price_per_day']

    # controlas that rating list metadata is correct
    assert response_json['amount'] == 2


def test_delete_existing_room(test_app):
    room_1_id = 1
    room_2_id = 2

    response_1 = test_app.delete(
        '/rooms/' + str(room_1_id)
    )

    response_2 = test_app.delete(
        '/rooms/' + str(room_2_id)
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    response_json_1 = response_1.json() 
    response_json_2 = response_2.json()

    assert response_json_1['id'] == room_1_id
    assert response_json_1['type'] == test_room_payload['type']
    assert response_json_1['owner'] == test_room_payload['owner']
    assert response_json_1['owner_id'] == test_room_payload['owner_id']
    assert response_json_1['price_per_day'] == test_room_payload['price_per_day']

    assert response_json_2['id'] == room_2_id
    assert response_json_2['type'] == test_another_room_payload['type']
    assert response_json_2['owner'] == test_another_room_payload['owner']
    assert response_json_2['owner_id'] == test_another_room_payload['owner_id']
    assert response_json_2['price_per_day'] == test_another_room_payload['price_per_day']


def test_delete_not_existent_room(test_app):
    non_existent_room_id = 25

    response = test_app.delete(
        '/rooms/' + str(non_existent_room_id)
    )

    assert response.status_code == 404

    response_json = response.json() 

    assert response_json['error'] == 'not found'

