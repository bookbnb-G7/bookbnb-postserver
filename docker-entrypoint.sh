#!/bin/sh
cd postserver/
daphne -b 0.0.0.0 -p ${PORT:-5000} app.main:app
