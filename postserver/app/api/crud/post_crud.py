from app.db import posts_table, database
from app.api.models.post_model import PostSchema

async def post(payload: PostSchema):
    query = posts_table.insert().values(title=payload.title, 
    	                       		    body=payload.body,
    	                                author=payload.author)

    return await database.execute(query=query)


async def get(post_id: int):
    query = posts_table.select().where(post_id == posts_table.c.id)
    return await database.fetch_one(query=query)
