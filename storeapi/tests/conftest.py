import os
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from fastapi.testclient import TestClient

# from storeapi.routers.post_router import comment_table, user_table

os.environ["ENV_STATE"] = "test"
from storeapi.database import database  # noqa: E402
from storeapi.main import app  # noqa: E402


# run once per session
@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


# run every time a test is run
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    database.connect()
    #    user_table.clear()
    #    comment_table.clear()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:  # client() runs first
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
