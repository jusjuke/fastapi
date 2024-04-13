import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.post_router import router as post_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting the application")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(post_router)


@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code}, {exc.detail}")
    return await http_exception_handler(request, exc)


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
