from fastapi import FastAPI
from app.db import Base, engine
from app.api.routes import room_router, room_review_router, room_rating_router

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def pong():
    return {"message": "postserver"}

app.include_router(room_router.router, prefix="/rooms", tags=["rooms"])
app.include_router(room_review_router.router, prefix="/rooms/{room_id}/reviews", tags=['reviews'])
app.include_router(room_rating_router.router, prefix="/rooms/{room_id}/ratings", tags=['ratings'])