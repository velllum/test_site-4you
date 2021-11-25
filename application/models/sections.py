import enum
from typing import Optional, List
from datetime import datetime
from pydantic import (
    BaseModel,
    Field
)
from .base import (
    SuccessResponse,
    ListData
)
from models.tracks import (
    Track
)


class SectionType(str, enum.Enum):
    ADVERT = 'advert'
    PROGRAM = 'program'
    STREAM = 'stream'


class Section(BaseModel):
    id: int
    radio_id: int
    name: str 
    type: SectionType
    color: str 
    en: bool
    tracks_in: List[Track]
    tracks_out: List[Track]
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class SectionListData(ListData):
    items: List[Section] = []


class SectionSuccessResponse(SuccessResponse):
    data: Section


class SectionListSuccessResponse(SuccessResponse):
    data: SectionListData


class NewSection(BaseModel):
    name: str
    color: str
    type: SectionType
    tracks_in: List[int] = []
    tracks_out: List[int] = []