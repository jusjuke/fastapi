from fastapi import APIRouter, HTTPException
from storeapi.models.user import (
    CommentIn,
    CommentOut,
    UserPostIn,
    UserPostOut,
    UserPostWithComments,
)

router = APIRouter()
user_table = {}
comment_table = {}


def find_user(post_id: int):
    return user_table.get(post_id)


def find_comment_by_postid(post_id: int):
    return comment_table.get(post_id)


@router.post("/post", response_model=UserPostOut, status_code=201)
async def create_post(item: UserPostIn):
    id = len(user_table) + 1
    userPostOut = {**item.model_dump(), "id": id}
    user_table[id] = userPostOut
    return userPostOut


@router.get("/post", response_model=list[UserPostOut])
async def read_posts():
    return list(user_table.values())


@router.post("/comment", response_model=CommentOut, status_code=201)
async def create_comment(item: CommentIn):
    id = len(comment_table) + 1
    user = find_user(item.post_id)
    if not user:
        raise HTTPException(status_code=404, detail="Post not found")
    userCommentOut = {**item.model_dump(), "id": id}
    #    userCommentOut["post_id"] = user["id"]
    comment_table[id] = userCommentOut
    return userCommentOut


@router.get("/post/{post_id}/comment", response_model=list[CommentOut])
async def read_comment_by_postid(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def read_post_by_id(post_id: int):
    user = find_user(post_id)
    if not user:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": user, "comments": await read_comment_by_postid(post_id)}
