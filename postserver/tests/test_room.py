import json

test_room_payload = {
    'type': 'traphouse', 
    'owner': 'facu, el crack',
    'owner_id': 1,
    'price_per_day': 1800.0
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


def test_delete_existing_room(test_app):
    room_id = 1

    response = test_app.delete(
        '/rooms/' + str(room_id)
    )

    assert response.status_code == 200

    response_json = response.json() 

    assert response_json['id'] == 1 
    assert response_json['type'] == test_room_payload['type']
    assert response_json['owner'] == test_room_payload['owner']
    assert response_json['owner_id'] == test_room_payload['owner_id']
    assert response_json['price_per_day'] == test_room_payload['price_per_day']
