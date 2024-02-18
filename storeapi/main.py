from contextlib import asynccontextmanager

from fastapi import FastAPI
from storeapi.database import database
from storeapi.routers.post_router import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post_router)


# from fastapi import FastAPI
# from storeapi.models.user import UserPostIn, UserPostOut


# app = FastAPI()
# user_table = {}


# @app.post("/post", response_model=UserPostOut)
# async def create_post(item: UserPostIn):
#     id = len(user_table) + 1
#     userPostOut = {**item.model_dump(), "id": id}
#     user_table[id] = userPostOut
#     return userPostOut


# @app.get("/post", response_model=list[UserPostOut])
# async def read_posts():
#     return list(user_table.values())


# @app.get("/")
# async def root():
#    return {
#        "message": "Hello World",
#        "long": " dfdfdsdsdsddddsds dfdfdsdsdsddddsd",
#    }
