from datetime import datetime
import enum
from typing import Optional, Union, List

from pydantic import (
    BaseModel,
    Field
)


class Role(str, enum.Enum):
    ADMIN = 'admin'
    OWNER = 'owner'
    MANAGER = 'manager'
    TRAFFIC_MANAGER = 'traffic_manager'
    CLIENT = 'client'


class UserRadio(BaseModel):
    id: int
    radio_id: int
    user_id: int
    role: Role
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class NewUserRadio(BaseModel):
    radio_id: int
    user_id: int
    role: Role
    en: bool = True