from typing import Optional, List
import enum
from datetime import datetime
from pydantic import (
    BaseModel, 
    Field,
    conint
)
from .base import (
    SuccessResponse,
    ListData
)
from .sections import (
    Section
)


MAX_HOUR_SECONDS = 3600


class BlockType(str, enum.Enum):
    TIME = 'time'
    DTMF = 'dtmf'


class Block(BaseModel):
    id: int = 0
    radio_id: int 
    name: str
    type: BlockType
    color: str
    sections: List[Section]
    time_start: conint(ge=0, le=MAX_HOUR_SECONDS)
    time_delta: int
    len: conint(ge=1, le=MAX_HOUR_SECONDS)
    dtmf_in: List[str]
    dtmf_out: List[str]
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class BlockSuccessResponse(SuccessResponse):
    data: Block


class BlockListData(ListData):
    items: List[Block] = []


class BlockListSuccessResponse(SuccessResponse):
    data: BlockListData


class NewBlock(BaseModel):
    name: str
    type: BlockType
    color: str
    sections: List[int]
    time_start: conint(ge=0, le=MAX_HOUR_SECONDS)
    time_delta: int
    len: conint(ge=1, le=MAX_HOUR_SECONDS)
    dtmf_in: List[str] = []
    dtmf_out: List[str] = []
    en: bool = True