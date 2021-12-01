from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    """- Базовый класс пользователя"""
    name: str
    surname: str
    middle_name: str
    email: str
    # created_date: Optional[datetime]
    # updated_date: Optional[datetime]


class User(BaseUser):
    """- Класс пользователя"""
    id: int

    class Config:
        orm_mode = True


class CreateUser(BaseUser):
    """- Создать пользователя"""
    password: str


class UpdateUser(BaseUser):
    """- Обновить пользователя"""
    password: str


class DeleteUser(BaseUser):
    """- Обновить пользователя"""
    pass
