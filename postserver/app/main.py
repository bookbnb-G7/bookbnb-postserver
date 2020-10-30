from fastapi import FastAPI
from app.api.routes import room_router
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def pong():
    return {"message": "postserver"}

app.include_router(room_router.router, prefix="/rooms", tags=["rooms"])