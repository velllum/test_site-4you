from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .base import (
    SuccessResponse,
    ListData
)


class Preset(BaseModel):
    id: int
    user_id: int
    name: str
    stream_id: int
    tz: int
    city: str
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class PresetListData(ListData):
    items: List[Preset]


class PresetListSuccessResponse(SuccessResponse):
    data: PresetListData