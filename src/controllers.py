import httpx
from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from src.models import User, Post, User_Pydantic, Post_Pydantic


async def init_tortoise():
    await Tortoise.init(
        db_url='sqlite://database.db',
        modules={'modules': ['src.models']}
    )
    await Tortoise.generate_schemas()


class UserRepository:
    @classmethod
    async def add_one(cls, users_data: dict) -> None:
        await init_tortoise()
        try:
            for user in users_data:
                await User.create(
                    id=user['id'],
                    name=user['name'],
                    email=user['email'],
                    gender=user['gender'],
                    status=user['status']
                )
        except IntegrityError:
            ...
        finally:
            await Tortoise.close_connections()

    @classmethod
    async def read_all(cls):
        return await User_Pydantic.from_queryset(User.all())

    @classmethod
    async def read_one(cls, user_id: int) -> User_Pydantic:
        return await User_Pydantic.from_queryset_single(User.get(id=user_id))


class PostRepository:
    @classmethod
    async def add_one(cls, post_data: dict) -> None:
        await init_tortoise()
        try:
            for post in post_data:
                await Post.create(
                    id=post['id'],
                    user_id=post['user_id'],
                    title=post['title'],
                    body=post['body'],
                )
        except IntegrityError:
            ...
        finally:
            await Tortoise.close_connections()

    @classmethod
    async def read_one(cls, user_id: int = None):
        if user_id:
            return await Post_Pydantic.from_queryset(Post.filter(user_id=user_id))

        return await Post_Pydantic.from_queryset(Post.all())


async def get_and_save_data():
    async with httpx.AsyncClient() as client:
        users_url = 'https://gorest.co.in/public/v2/users'
        comments_url = 'https://gorest.co.in/public/v2/posts'

        urls = []
        for url in [users_url, comments_url]:
            response = await client.get(url)
            if response.status_code == 200:
                urls.append(response.json())

        await UserRepository.add_one(urls[0])
        await PostRepository.add_one(urls[1])

        return {'status': response.status_code}
