from typing import List, Optional

from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .message import MessageService
from ..database import db
from ..models import users as ml
from ..schemas import users as sm


class BaseService:
    """- базовый класс сервиса"""

    def __init__(self, session: Session = Depends(db.get_db)):
        self.session = session

    def _get(self, user_id: int) -> Optional[ml.User]:
        """- получить пользователя,
        - если пользователь отсутствует отправляем ошибку 404"""
        user = self.session.query(ml.User).get(user_id)

        if not user:
            raise MessageService.error_404("Пользователь с данным ID не найден")

        return user


class UserService(BaseService):
    """- Пользовательский сервис"""

    def get_list(self) -> List[ml.User]:
        """- получить список пользователей"""
        return self.session.query(ml.User).all()

    def get_by_id(self, user_id: int) -> Optional[ml.User]:
        """- получить пользователя по id"""
        return self._get(user_id)

    def create(self, user_data: sm.CreateUser) -> ml.User:
        """- создать пользователя"""

        # проверяем если email существует вызываем исключение
        if self.session.query(ml.User).filter(ml.User.email == user_data.email).first():
            raise MessageService.error_404("Пользователь с таким email зарегистрирован")

        user = ml.User(**user_data.dict())
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, user_data: sm.UpdateUser) -> ml.User:
        """- обновить пользователя"""
        user = self._get(user_id)
        self.session.query(ml.User).filter_by(id=user.id).update(user_data.dict())
        self.session.commit()

        return user

    def delete(self, user_id: int):
        """- удалить пользователя"""
        user = self._get(user_id)
        self.session.delete(user)
        self.session.commit()

    def search(self, query_string: str) -> Optional[List[ml.User]]:
        """- поиск по полям"""
        query = self.session.query(ml.User).filter(
            or_(
                ml.User.name.contains(query_string),
                ml.User.surname.contains(query_string),
                ml.User.middle_name.contains(query_string),
                ml.User.email.contains(query_string),
            )
        ).all()

        if not query:
            raise MessageService.error_404("Ничего не найдено, попробуйте еще раз")

        return query
