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
from models.storage import (
    Storage
)
from models.categories import (
    Category
)


class PlayRuleType(str, enum.Enum):
    SEQUENCE = 'sequence'
    RANDOM = 'random'
    TOGETHER = 'together'


class GroupPosType(str, enum.Enum):
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'
    TOP = 'top'
    LIST = 'list'
    BOTTOM = 'bottom'
    THIRD_BOTTOM = 'third_bottom'
    SECOND_BOTTOM = 'second_bottom'
    FIRST_BOTTOM = 'first_bottom'


class Track(BaseModel):
    id: int
    radio_id: int
    name: str 
    rds_text: str
    category: Optional[Category]
    play_rule: PlayRuleType
    group_pos: GroupPosType
    storages: List[Storage]
    pos: int
    played_count: int
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class TrackListData(ListData):
    items: List[Track] = []


class TrackSuccessResponse(SuccessResponse):
    data: Track


class TrackListSuccessResponse(SuccessResponse):
    data: TrackListData


class NewTrack(BaseModel):
    name: str 
    rds_text: str
    category_id: Optional[int] = Field(None, nullable=True)
    play_rule: PlayRuleType
    group_pos: GroupPosType
    storage_ids: List[int]
    pos: int
