import pytest
from httpx import AsyncClient


async def create_post(body: str, client: AsyncClient) -> dict:
    response = await client.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, client: AsyncClient) -> dict:
    response = await client.post("/comment", json={"body": body, "post_id": post_id})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("test post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("test comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    response = await async_client.post("/post", json={"body": "test post"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "body": "test post"}
    assert {"id": 1, "body": "test post"}.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")
    assert response.status_code == 200
    print(response.json())
    print([created_post])
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    response = await async_client.post(
        "/comment", json={"body": "test comment", "post_id": created_post["id"]}
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "body": "test comment",
        "post_id": created_post["id"],
    }


@pytest.mark.anyio
async def test_get_comment_by_post_id(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    print(created_comment)
    print(response.json())
    assert response.json() == [created_comment]


# pytest --fixtures
# pytest --v
