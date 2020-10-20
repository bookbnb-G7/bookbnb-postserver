from fastapi import FastAPI
from app.api.routes import post_route
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
async def initial():
    return {"message": "postserver"}

app.include_router(post_route.router, prefix="/posts", tags=["posts"])
