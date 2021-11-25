from typing import Optional, List
import enum
from datetime import datetime
from pydantic import (
    BaseModel, 
    validator, 
    Field
)
from .base import (
    SuccessResponse,
    ListData
)


class StreamInfoType(str, enum.Enum):
    STREAM = 'stream'


class Stream(BaseModel):
    id: int
    name: str
    urls: List[str] = []
    locale: str = 'en_US.UTF-8'
    info_type: StreamInfoType = StreamInfoType.STREAM
    info_url: str
    sound_processing_template: str = 'default'
    en: bool = True
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class StreamShort(BaseModel):
    id: int
    name: str

    
class StreamSuccessResponse(SuccessResponse):
    data: Stream


class StreamListData(ListData):
    items: List[Stream] = []


class StreamShortListData(ListData):
    items: List[StreamShort] = []


class StreamListSuccessResponse(SuccessResponse):
    data: StreamListData


class StreamShortListSuccessResponse(SuccessResponse):
    data: StreamShortListData


class NewStream(BaseModel):
    name: str
    urls: List[str] = []
    locale: str = 'en_US.UTF-8'
    info_type: StreamInfoType = StreamInfoType.STREAM
    info_url: str
    sound_processing_template: str = 'default'
    en: bool = True

