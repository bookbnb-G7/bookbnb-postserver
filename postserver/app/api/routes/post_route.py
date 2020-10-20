from app.api.crud import post_crud
from fastapi import APIRouter, HTTPException
from app.api.models.post_model import PostDB, PostSchema

router = APIRouter()

@router.post("/", response_model=PostDB, status_code=201)
async def create_post(payload: PostSchema):
    post_id = await post_crud.post(payload)

    response_post = {
        "id": post_id,
        "title": payload.title,
        "body": payload.body,
        "author": payload.author
    }

    return response_post


@router.get("/{post_id}/", response_model=PostDB, status_code=200)
async def read_post(post_id: int):
    post = await post_crud.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
