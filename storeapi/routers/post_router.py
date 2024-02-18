from fastapi import APIRouter, HTTPException
from storeapi.database import comment_table, database, post_table
from storeapi.models.user import (
    CommentIn,
    CommentOut,
    UserPostIn,
    UserPostOut,
    UserPostWithComments,
)

router = APIRouter()
# user_table = {}
# comment_table = {}


async def find_user(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


def find_comment_by_postid(post_id: int):
    return comment_table.get(post_id)


@router.post("/post", response_model=UserPostOut, status_code=201)
async def create_post(item: UserPostIn):
    data = item.model_dump()
    query = post_table.insert().values(data)
    print(query)
    last_insert_id = await database.execute(query)
    return {**data, "id": last_insert_id}
    #    id = len(user_table) + 1
    #    userPostOut = {**item.model_dump(), "id": id}
    #    user_table[id] = userPostOut
    # return userPostOut


@router.get("/post", response_model=list[UserPostOut])
async def read_posts():
    return await get_all_posts()  # list(post_table.values())


@router.post("/comment", response_model=CommentOut, status_code=201)
async def create_comment(item: CommentIn):
    post = await find_user(item.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = item.model_dump()
    query = comment_table.insert().values(data)
    last_insert_id = await database.execute(query)
    return {**data, "id": last_insert_id}
    # id = len(comment_table) + 1
    # user = find_user(item.post_id)
    # if not user:
    #    raise HTTPException(status_code=404, detail="Post not found")
    # userCommentOut = {**item.model_dump(), "id": id}
    #    userCommentOut["post_id"] = user["id"]
    # comment_table[id] = userCommentOut
    # return userCommentOut


@router.get("/post/{post_id}/comment", response_model=list[CommentOut])
async def read_comment_by_postid(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


#    return [
#        comment for comment in comment_table.values() if comment["post_id"] == post_id
#    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def read_post_by_id(post_id: int):
    user = find_user(post_id)
    if not user:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": user, "comments": await read_comment_by_postid(post_id)}
