from typing import List

from fastapi import APIRouter, Depends

from ..schemas import users as sm
from ..services.users import UserService

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[sm.User])
async def index(session: UserService = Depends()) -> List[sm.User]:
    """- индексная страница пользователя
    ../api/v2/users/"""
    return session.get_list()
