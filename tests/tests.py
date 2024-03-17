from httpx import AsyncClient
from src.models import User


async def test_get_users(client: AsyncClient):
    response = await client.get("/api/users/all_users/")
    assert response.status_code == 200

    user_obj = await User.get(id=6787701)
    assert user_obj.id == 6787701


async def test_get_user(client: AsyncClient):
    response = await client.get("/api/users/6787704")
    assert response.status_code == 200


async def test_get_posts(client: AsyncClient):
    response = await client.get("/api/posts", params={'user_id': 6787718})
    assert response.status_code == 200
