from fastapi import FastAPI
from app.api.routes import room_router
from app.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def pong():
    return {"message": "postserver"}

app.include_router(room_router.router, prefix="/rooms", tags=["rooms"])