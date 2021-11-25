from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .base import (
    SuccessResponse,
    ListData
)
from models.blocks import (
    Block
)


class HourPlan(BaseModel):
    id: int
    radio_id: int 
    name: str 
    is_default: bool
    blocks: List[Block]
    color: str 
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class HourPlanListData(ListData):
    items: List[HourPlan]


class HourPlanSuccessResponse(SuccessResponse):
    data: HourPlan


class HourPlanListSuccessResponse(SuccessResponse):
    data: HourPlanListData


class NewHourPlan(BaseModel):
    name: str
    color: str
    blocks: List[int]
