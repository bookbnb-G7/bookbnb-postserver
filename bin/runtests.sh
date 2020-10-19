#!/bin/sh

docker-compose up -d
docker exec bookbnb-postserver_web bash -c 'while !</dev/tcp/db/5432; do sleep 1; done;'
docker exec bookbnb-postserver_web pytest --cov=postserver --color=yes
docker exec bookbnb-postserver_web pylint postserver
docker-compose down
