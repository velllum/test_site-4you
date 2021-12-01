from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .. import ErrorResponse
from ..database import db
from ..models import users as ml
from ..schemas import users as sm


class UserService:
    """- Пользовательский сервис,
     для хранения логики"""

    def __init__(self, session: Session = Depends(db.get_db)):
        self.session = session

    def _save(self, obj):
        """- сохранить в базу"""
        self.session.add(obj)
        self.session.commit()

    def _get(self, user_id: int) -> Optional[ml.User]:
        response = self.session.query(ml.User).filter(ml.User.id == user_id).first()
        if not response:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                # detail=ErrorResponse,
            )
        return response

    def get_list(self) -> List[ml.User]:
        """- получить список пользователей"""
        return self.session.query(ml.User).all()

    def get_by_id(self, user_id: int) -> Optional[ml.User]:
        """- получить пользлователя по id"""
        return self._get(user_id)

    def create(self, user_create: sm.CreateUser) -> ml.User:
        """- создать пользователя"""
        user = ml.User(**user_create.dict())
        self._save(user)
        return user
