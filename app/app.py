import uuid
import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostUpdate, PostResponse

app = FastAPI()

# In-memory store: {uuid: dict}
posts: dict[uuid.UUID, dict] = {}


@app.get("/posts", response_model=List[PostResponse])
def get_all_posts():
    return [{"id": post_id, **data} for post_id, data in posts.items()]


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: uuid.UUID):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"id": post_id, **posts[post_id]}


@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate):
    post_id = uuid.uuid4()
    posts[post_id] = {
        "caption": post.caption,
        "url": post.url,
        "file_type": post.file_type,
        "file_name": post.file_name,
    }
    return {"id": post_id, **posts[post_id]}


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: uuid.UUID, post: PostUpdate):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    stored = posts[post_id]
    updated = post.model_dump(exclude_unset=True)
    stored.update(updated)
    posts[post_id] = stored
    return {"id": post_id, **stored}


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: uuid.UUID):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]
