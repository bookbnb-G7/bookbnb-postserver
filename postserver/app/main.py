import logging
from fastapi import FastAPI
from app.db import Base, engine
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from app.errors.auth_error import AuthException
from app.errors.bookbnb_error import BookbnbException
from app.api.routes import (room_photo_router, room_rating_router,
                            room_review_router, room_router,
                            room_booking_router,room_comment_router)

Base.metadata.create_all(engine)

app = FastAPI(
    title="bookbnb-postserver", description="postserver API"
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc):
    error = {"error": exc.detail}
    logging.error(f"status code: {exc.status_code} message: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(BookbnbException)
async def bookbnb_exception_handler(_request, exc):
    error = {"error": exc.detail}
    logging.error(f"status code: {exc.status_code} message: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(AuthException)
async def auth_exception_handler(_request, exc):
    error = {"error": exc.detail}
    logging.error(f"status code: {exc.status_code} message: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=error)


app.include_router(
    room_router.router, prefix="/rooms", tags=["rooms"]
)

app.include_router(
    room_photo_router.router, prefix="/rooms/{room_id}/photos", tags=["photos"]
)

app.include_router(
    room_review_router.router, prefix="/rooms/{room_id}/reviews", tags=["reviews"]
)

app.include_router(
    room_rating_router.router, prefix="/rooms/{room_id}/ratings", tags=["ratings"]
)

app.include_router(
    room_booking_router.router, prefix="/rooms/{room_id}/bookings", tags=["bookings"]
)

app.include_router(
    room_comment_router.router, prefix="/rooms/{room_id}/comments", tags=["coments"]
)
