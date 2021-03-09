#!/bin/sh
cd postserver/
uvicorn app.main:app --reload --workers 4 --host 0.0.0.0 --port 8080