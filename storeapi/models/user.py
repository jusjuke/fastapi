from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPostOut(UserPostIn):
    id: int


class CommentIn(BaseModel):
    post_id: int
    body: str


class CommentOut(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPostOut
    comments: list[CommentOut]


# {'post': {'body': 'This is a post', 'id': 1},
# 'comments': [{'post_id': 1, 'body': 'This is a comment', 'id': 1},{'post_id': 1, 'body': 'This is a comment', 'id': 2}]
