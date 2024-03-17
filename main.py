from typing import List
from fastapi import FastAPI
from tortoise.exceptions import IntegrityError

from models import User_Pydantic, User, Comment
import httpx
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
import asyncio

app = FastAPI(title="Project for SpaceLab")


async def init_tortoise():
    await Tortoise.init(
        db_url='sqlite://database.db',
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()


async def save_users_to_database(users_data):
    await init_tortoise()
    try:
        for user_data in users_data:
            await User.create(
                id=user_data.get('id'),
                name=user_data.get('name'),
                email=user_data.get('email'),
                gender=user_data.get('gender'),
                status=user_data.get('status')
            )
    except IntegrityError:
        return 'This data is already exists'
    finally:
        await Tortoise.close_connections()


async def save_comments_to_database(comments_data):
    await init_tortoise()
    try:
        for comm in comments_data:
            await Comment.create(
                id=comm.get('id'),
                post_id=comm.get('post_id'),
                name=comm.get('name'),
                email=comm.get('email'),
                body=comm.get('body')
            )
    except IntegrityError:
        return 'This data is already exists'
    finally:
        await Tortoise.close_connections()


async def get_and_save_data():
    await init_tortoise()
    async with httpx.AsyncClient() as client:
        url = 'https://gorest.co.in/public/v2/users'
        url_comments = 'https://gorest.co.in/public/v2/comments'
        response = await client.get(url)
        response_comments = await client.get(url_comments)

        response.raise_for_status()

        json = [response.json(), response_comments.json()]

        if response.status_code == 200:
            await asyncio.gather(
                save_users_to_database(json[0]),
                save_comments_to_database(json[1])
            )
            return {'status': response.status_code, 'detail': json}


@app.on_event("startup")
async def startup_event():
    await get_and_save_data()


@app.get('/users/all_users/', response_model=List[User_Pydantic])
async def get_all_users():
    return await User_Pydantic.from_queryset(User.all())


@app.get('/users/{user_id}', response_model=User_Pydantic)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@app.get('/comments/{id}', response_model=str)
async def get_comment_by_id(id: int):
    comm_obj = await Comment.get(id=id)
    if comm_obj:
        return comm_obj.body


register_tortoise(
    app,
    db_url="sqlite://database.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
