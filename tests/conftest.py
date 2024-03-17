import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from main import app


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
