from typing import List, Optional

from fastapi import APIRouter, Depends, Response, Query
from starlette import status
from starlette.responses import Response

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
    """- получить список всех пользователей
    ../api/v1/users/"""
    return session.get_list()


@router.get('/{user_id}', response_model=sm.User)
async def user(
    user_id: int,
    session: UserService = Depends()
) -> sm.User:
    """- получить пользователя по его id
    ../api/v1/user/{user_id}"""
    return session.get_by_id(user_id)


@router.post('/create', response_model=sm.User)
async def user_create(
    user_data: sm.CreateUser,
    session: UserService = Depends()
):
    """- создать пользователя
    ../api/v1/user/create"""
    return session.create(user_data)


@router.put('/{user_id}', response_model=sm.User)
async def user_update(
    user_id: int,
    user_data: sm.UpdateUser,
    session: UserService = Depends()
):
    """- обновить пользователя
    ../api/v1/user/{PUT: user_id}"""
    return session.update(user_id, user_data)


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def user_delete(
    user_id: int,
    session: UserService = Depends()
):
    """- удалить пользователя
    ../api/v1/user/{DELETE: user_id}"""
    session.delete(user_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content="Пользователь был удален"
    )


@router.get('/search/', response_model=Optional[List[sm.User]], status_code=status.HTTP_200_OK)
async def user_search(
    q: str = Query(..., description="User search"),
    session: UserService = Depends()
):
    """- поиск пользователей
    ../api/v1/user/search?q={q}"""
    query = session.search(q)
    if not query:
        return Response(
            status_code=status.HTTP_200_OK,
            content="Ничего не найдено, попробуйте еще раз"
        )

    return query
