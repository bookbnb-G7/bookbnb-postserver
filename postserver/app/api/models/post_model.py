from pydantic import BaseModel
from datetime import datetime

class PostSchema(BaseModel):
    title: str
    body: str
    author: str

class PostDB(PostSchema):
    id: int
