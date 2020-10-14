#!/bin/sh
cd postserver/
uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
