#!/bin/sh
cd postserver/
daphne -b 0.0.0.0 -p 8080 app.main:app