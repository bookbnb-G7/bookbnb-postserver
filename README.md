# bookbnb-postserver

[![Build Status](https://travis-ci.com/bookbnb-G7/bookbnb-postserver.svg?branch=develop)](https://travis-ci.com/bookbnb-G7/bookbnb-postserver)
[![Coverage Status](https://coveralls.io/repos/github/bookbnb-G7/bookbnb-postserver/badge.svg?branch=develop)](https://coveralls.io/github/bookbnb-G7/bookbnb-postserver?branch=develop)

# Run Tests
`bin/runtest.sh`

# Start local version

## Building and running:
`bin/server.sh up build`

## Running without building:
`bin/server.sh up`

## Pause server:
`bin/server.sh stop`

## Resume server
`bin/server.sh start`

## Stop server and removing local database volume
`bin/server.sh down volume`

## Stop server without preserving local database data
`bin/server.sh down`

# Removing Images, Containes and Volumes associated
`bin/armagedon.sh`
