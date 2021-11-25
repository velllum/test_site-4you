from typing import Optional, List
from datetime import datetime
import enum
from pydantic import (
    BaseModel,
    Field
)
from .base import (
    SuccessResponse,
    ListData
)
from .sound_template import BaseConfigGain


class RadioType(str, enum.Enum):
    NULL = 'null'
    STREAM = 'stream'
    DEVICE = 'device'
    PRESET = 'preset'


class UpdatableRadioType(str, enum.Enum):
    STREAM = 'stream'
    DEVICE = 'device'


class Radio(BaseModel):
    id: int
    user_id: int
    name: str
    type: RadioType
    stream_id: Optional[int] = Field(None, nullable=True)
    tz: int
    city: str
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)   


class RadioSuccessResponse(SuccessResponse):
    data: Radio


class RadioWithConfig(Radio):
    sound_processing_template: str
    sound_processing_config: BaseConfigGain


class RadioListData(ListData):
    items: List[Radio] = []


class RadioListSuccessResponse(SuccessResponse):
    data: RadioListData


class NewRadioBase(BaseModel):
    name: str
    city: str
    tz: int
    type: UpdatableRadioType


class NewRadio(NewRadioBase):
    stream_id: Optional[int] = Field(None, nullable=True)


class NewStreamRadio(NewRadioBase):
    stream_id: int


class NewPresetRadio(NewRadioBase):
    preset_id: int


class NewUrlsRadio(NewRadioBase):
    urls: List[str]


class UpdateRadio(BaseModel):
    name: str
    city: str
    type: UpdatableRadioType
    tz: int
