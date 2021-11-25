from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import (
    BaseModel,
    validator,
    Field
)
from models.base import (
    SuccessResponse,
    ListData
)

class FileProcessingType(str, Enum):
    DEFAULT = "processing"
    ONLY_CONVERT = "only_convert"


class StorageStateType(str, Enum):
    JUST_ADDED = 'just_added'
    PROCESSING = 'processing'
    READY = 'ready'


class StorageType(str, Enum):
    FILE = "file"
    FOLDER = "folder"


class BaseItem(BaseModel):
    radio_id: Optional[int] = Field(None, nullable=True)
    pid: int = 0
    state: StorageStateType = StorageStateType.JUST_ADDED
    type: StorageType
    name: str
    location: str = ""
    user_id: int
    duration: int = 0
    version: int = 1
    en: bool = False
    

class Storage(BaseItem):
    id: int
    url: Optional[str] = Field(None, nullable=True)
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class StorageSuccessResponse(SuccessResponse):
    data: Storage


class ItemAddInternal(BaseItem):
    id: Optional[int]


class StorageList(BaseModel):
    __root__: List[Storage]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class StorageListData(ListData):
    items: List[Storage]



class StorageListSuccessResponse(SuccessResponse):
    data: StorageListData


class ItemUpdateExternal(BaseModel):
    pid: Optional[int] = Field(None, nullable=True)
    name: Optional[str] = Field(None, nullable=True)


class ItemUpdateInternal(BaseModel):
    pid: Optional[int] = Field(None, nullable=True)
    state: Optional[StorageStateType] = Field(None, nullable=True)
    type: Optional[StorageType] = Field(None, nullable=True)
    name: Optional[str] = Field(None, nullable=True)
    location: Optional[str] = Field(None, nullable=True)
    user_id: Optional[int] = Field(None, nullable=True)
    duration: Optional[int] = Field(None, nullable=True)
    version: Optional[int] = Field(None, nullable=True)
    en: Optional[bool] = Field(None, nullable=True)


class FolderAdd(BaseModel):
    name: str
