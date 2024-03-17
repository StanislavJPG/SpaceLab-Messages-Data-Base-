from typing import List

from fastapi import APIRouter

from src.controllers import UserRepository, PostRepository
from src.models import User_Pydantic, Post_Pydantic

router = APIRouter(prefix='/api')


@router.get('/users/all_users/', response_model=List[User_Pydantic])
async def get_all_users() -> UserRepository:
    return await UserRepository.read_all()


@router.get('/users/{user_id}', response_model=User_Pydantic)
async def get_user(user_id: int):
    return await UserRepository.read_one(user_id)


@router.get('/comments', response_model=Post_Pydantic)
async def get_comment_by_id(user_id: int = None):
    return await PostRepository.read_one(user_id=user_id)
