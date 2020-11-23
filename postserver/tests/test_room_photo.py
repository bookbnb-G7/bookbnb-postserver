import json

test_room_payload = {
	'type': 'traphouse', 
	'owner': 'facu, el crack',
	'owner_id': 1,
	'price_per_day': 1800.0
}

room_id = 1

test_room_photo_payload = {
	'url': 'www.queganasdesalirdejoda.com',
	'firebase_id': 1
}

test_another_room_photo_payload = {
	'url': 'www.sigoconganasdesalirdejoda.com',
	'firebase_id': 2
}

def _create_room(test_app):
	test_app.post(
		'/rooms/',
		data = json.dumps(test_room_payload)
	)

def _delete_room(test_app):
	test_app.delete(
		'/rooms/' + str(room_id)
	)

def test_upload_photo_for_existing_room(test_app):
	_create_room(test_app)

	response = test_app.post(
		'/rooms/' + str(room_id) + '/photos/',
		data = json.dumps(test_room_photo_payload)
	)

	assert response.status_code == 201

	response_json = response.json()
    
	assert response_json['id'] == 1
	assert response_json['url'] == test_room_photo_payload['url']
	assert response_json['firebase_id'] == test_room_photo_payload['firebase_id']

def test_get_existing_photo_from_room(test_app):
	firebase_id = test_room_photo_payload['firebase_id']

	response = test_app.get(
		'/rooms/' + str(room_id) + '/photos/' + str(firebase_id)
	)

	assert response.status_code == 200

	response_json = response.json()

	assert response_json['id'] == 1
	assert response_json['url'] == test_room_photo_payload['url']
	assert response_json['firebase_id'] == test_room_photo_payload['firebase_id']

def test_get_all_photos_from_room(test_app):
	test_app.post(
		'/rooms/' + str(room_id) + '/photos/',
		data = json.dumps(test_another_room_photo_payload)
	)

	response = test_app.get(
		'/rooms/' + str(room_id) + '/photos/'
	)
	
	assert response.status_code == 200

	response_json = response.json()
    
	frt_photo = response_json['room_photos'][0]
	snd_photo = response_json['room_photos'][1] 

    # control that first photo is correct
	assert frt_photo['id'] == 1 
	assert frt_photo['url'] == test_room_photo_payload['url']
	assert frt_photo['firebase_id'] == test_room_photo_payload['firebase_id']

	# control that first photo is correct
	assert snd_photo['id'] == 2
	assert snd_photo['url'] == test_another_room_photo_payload['url']
	assert snd_photo['firebase_id'] == test_another_room_photo_payload['firebase_id']

	# controlas that review list metadata is correct
	assert response_json['amount'] == 2
	assert response_json['room_id'] == room_id


def test_delete_existing_room_photos(test_app):	
	room_photo_1_id = 1
	room_photo_2_id = 2

	response_1 = test_app.delete(
		'/rooms/' + str(room_id) + '/photos/' + str(room_photo_1_id),
	)

	response_2 = test_app.delete(
		'/rooms/' + str(room_id) + '/photos/' + str(room_photo_2_id),
	)

	assert response_1.status_code == 200
	assert response_2.status_code == 200

	response_json_1 = response_1.json()
	response_json_2 = response_2.json()    

	assert response_json_1['id'] == 1 
	assert response_json_1['url'] == test_room_photo_payload['url']
	assert response_json_1['firebase_id'] == test_room_photo_payload['firebase_id']

	assert response_json_2['id'] == 2
	assert response_json_2['url'] == test_another_room_photo_payload['url']
	assert response_json_2['firebase_id'] == test_another_room_photo_payload['firebase_id']

	_delete_room(test_app)