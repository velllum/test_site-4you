from pydantic import BaseModel


class BaseUser(BaseModel):
    """- Базовый класс пользователя"""
    name: str
    surname: str
    middle_name: str
    email: str


class User(BaseUser):
    """- Класс пользователя"""
    id: int

    class Config:
        orm_mode = True


class SearchUser(User):
    """- Найти пользователя"""
    ...


class CreateUser(BaseUser):
    """- Создать пользователя"""
    password: str


class UpdateUser(BaseUser):
    """- Обновить пользователя"""
    password: str


class DeleteUser(BaseUser):
    """- Удалить пользователя"""
    ...
