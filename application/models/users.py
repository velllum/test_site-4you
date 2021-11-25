from datetime import datetime
import enum
from typing import Optional, List

from pydantic import (
    BaseModel,
    Field,
)


class UserAccountType(str, enum.Enum):
    MAIL = 'mail'
    PHONE = 'phone'


class UserAccount(BaseModel):
    id: int
    user_id: int
    t: UserAccountType = UserAccountType.MAIL
    login: str
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class BaseUser(BaseModel):
    id: int = 0
    parent_id: Optional[None] = Field(None, nullable=True)
    name: str = ''
    accounts: List[UserAccount] = []
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)

    @property
    def is_authenticated(self):
        return bool(self.id)

    def account_by_login(self, t, login):
        for i in self.accounts:
            if i.t == t and i.login == login:
                return i
        return None


class Anonymous(BaseUser):
    pass


class User(BaseUser):
    pass


