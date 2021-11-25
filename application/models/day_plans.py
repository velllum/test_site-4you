from typing import Optional, List
import enum
from datetime import datetime
from pydantic import BaseModel, Field, conlist
from .base import (
    SuccessResponse,
    ListData
)
from .hour_plans import (
    HourPlan
)


class DayPlanType(str, enum.Enum):
    WORKDAY = 'workday'
    WEEKEND = 'weekend'
    USER = 'user'


class DayPlan(BaseModel):
    id: int
    radio_id: int
    name: str
    type: DayPlanType
    hours: conlist(item_type=Optional[HourPlan], min_items=24, max_items=24)
    is_default: bool
    color: str 
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class DayPlanListData(ListData):
    items: List[DayPlan]


class DayPlanSuccessResponse(SuccessResponse):
    data: DayPlan


class DayPlanListSuccessResponse(SuccessResponse):
    data: DayPlanListData


class NewDayPlan(BaseModel):
    name: str
    type: DayPlanType
    hours: conlist(item_type=int, min_items=24, max_items=24)
    color: str
