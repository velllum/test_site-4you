import re
from datetime import datetime
from typing import Dict, Pattern

from fastapi import HTTPException
from pydantic import BaseModel, root_validator
from starlette import status


class BaseUser(BaseModel):
    """- Базовый класс пользователя"""
    name: str
    surname: str
    middle_name: str
    email: str


class ValidatorUser(BaseUser):
    """- проверка поля"""
    password: str

    @classmethod
    def is_pattern_valid(cls, field: str, pattern: Pattern) -> bool:
        """- проверка шаблона"""
        return bool(pattern.match(field))

    @root_validator
    def validator(cls, values: Dict):
        """- проверка валидности полей"""
        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-zA-Z].*)[0-9a-zA-Z]{6,}$')
        pattern_email = re.compile(r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$')

        if not cls.is_pattern_valid(
            field=values.get("password"),
            pattern=pattern_password
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пароль должен содержать не менее 6 символов, одну букву и одну цифру."
            )

        elif not cls.is_pattern_valid(
            field=values.get("email"),
            pattern=pattern_email
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Укажите email правильно."
            )

        return values


class User(BaseUser):
    """- Класс пользователя"""
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True


class CreateUser(ValidatorUser):
    """- Создать пользователя"""
    ...


class UpdateUser(ValidatorUser):
    """- Обновить пользователя"""
    ...


class DeleteUser(BaseUser):
    """- Удалить пользователя"""
    ...


class SearchUser(User):
    """- Найти пользователя"""
    ...
