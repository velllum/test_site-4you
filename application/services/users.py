from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import db
from ..models import users as ml


class UserService:
    """- Пользовательский сервис,
     для хранения логики"""

    def __init__(self, session: Session = Depends(db.get_db)):
        self.session = session

    def get_list(self) -> List:
        """- получить список пользователей"""
        return self.session.query(ml.User).all()
