from typing import List

from fastapi import APIRouter, Depends

from ..schemas import users as sm
from ..services.users import UserService

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[sm.User])
async def users(
    session: UserService = Depends()
) -> List[sm.User]:
    """- плучить список всех пользователей
    ../api/v1/users/"""
    return session.get_list()


@router.get('/{user_id}', response_model=sm.User)
async def user(
    user_id: int,
    session: UserService = Depends()
) -> sm.User:
    """- индексная страница пользователя
    ../api/v1/user/{id}"""
    return session.get_by_id(user_id)


@router.post('/create', response_model=sm.User)
async def create(
    user_create: sm.CreateUser,
    session: UserService = Depends()
):
    """- создать полльзователя
    ../api/v1/user/create"""
    return session.create(user_create)
