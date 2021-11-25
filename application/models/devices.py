import enum
from typing import Optional
from datetime import datetime
from pydantic import (
    BaseModel,
    Field
)
from .base import (
    SuccessResponse
)


class DeviceType(str, enum.Enum):
    PRE_TRANSMITTER = 'pre-transmitter'
    ARCHIVER = 'archiver'
    STREAMER = 'streamer'


class DeviceConfig(BaseModel):
    output_css: int = 255
    output_audio: int = 255
    output_audio_l: int = 255
    output_audio_r: int = 255
    output_rds: int = 25
    output_audio_l_r: int = 255
    output_pilot: int = 31
    switch_type: int = 0
    switch_interval: int = 60
    switch_count: int = 2
    switch_return: int = 1800


class Device(BaseModel):
    id: int
    radio_id: int
    user_id: int
    device_id: str
    type: DeviceType
    config: DeviceConfig
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class DeviceSuccessResponse(SuccessResponse):
    data: Device


class NewDevice(BaseModel):
    device_id: str
    type: DeviceType = DeviceType.PRE_TRANSMITTER
    config: DeviceConfig = DeviceConfig()

