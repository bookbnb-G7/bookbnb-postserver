#!/bin/bash

docker-compose up -d
docker exec -e ENVIRONMENT=testing bookbnb-postserver_web  bash -c 'while !</dev/tcp/db/5432; do sleep 1; done;'
docker exec -e ENVIRONMENT=testing bookbnb-postserver_web pytest --cov=postserver --color=yes

if [ ${1-"none"} == "lint" ]; then
	docker exec bookbnb-postserver_web pylint postserver
fi

docker-compose down

