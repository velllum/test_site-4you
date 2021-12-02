import re
from datetime import datetime

from pydantic import BaseModel, validator


class BaseUser(BaseModel):
    """- Базовый класс пользователя"""
    name: str
    surname: str
    middle_name: str
    email: str


class User(BaseUser):
    """- Класс пользователя"""
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True


class ValidatorUser(BaseUser):
    """- Валидировать поля"""
    password: str

    @validator('password')
    def username_alphanumeric(cls, v):
        """- проверка валидности пароля
        - должен содержать не мение 6 символов
        - должен имень хотябы одну буквы
        - болжен имень одну циффру"""
        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{6,}$')
        assert bool(pattern_password.match(v)), 'Пароль дожен содержать не мение 6 симвоолов, одну букву, одну цифру'
        return v


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
