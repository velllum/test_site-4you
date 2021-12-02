from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from starlette import status

from ..database import db
from ..models import users as ml
from ..schemas import users as sm


class UserService:
    """- Пользовательский сервис,
     для хранения логики"""

    def __init__(self, session: Session = Depends(db.get_db)):
        self.session = session

    def _get(self, user_id: int) -> Optional[ml.User]:
        """- получить пользователя,
        - если пользователь отсутствует отпровляем ошибку 404"""
        response = self.session.query(ml.User).get(user_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь с данным ID не найден"
            )
        return response

    def get_list(self) -> List[ml.User]:
        """- получить список пользователей"""
        return self.session.query(ml.User).all()

    def get_by_id(self, user_id: int) -> Optional[ml.User]:
        """- получить пользлователя по id"""
        return self._get(user_id)

    def create(self, user_data: sm.CreateUser) -> ml.User:
        """- создать пользователя"""
        user = ml.User(**user_data.dict())
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, user_data: sm.UpdateUser) -> ml.User:
        """- обновить пользователя"""
        user = self._get(user_id)

        for key, value in user_data:
            setattr(user, key, value)

        self.session.commit()
        return user

    def delete(self, user_id: int):
        """- удалить пользователя"""
        user = self._get(user_id)
        self.session.delete(user)
        self.session.commit()

    def search(self, query_string: str) -> Optional[List[ml.User]]:
        """- поиск по полям"""
        users = self.session.query(ml.User).filter(
            or_(
                ml.User.name.contains(query_string),
                ml.User.surname.contains(query_string),
                ml.User.middle_name.contains(query_string),
                ml.User.email.contains(query_string),
            )
        ).all()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Ничего не найдено, попробуйте еще раз"
            )

        return users
