from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field
from .base import (
    SuccessResponse,
    ListData
)
from models.day_plans import DayPlan


class CalendarPlan(BaseModel):
    id: int
    radio_id: int 
    user_id: int 
    day_of: date
    day_plan: DayPlan
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class CalendarPlanSuccessResponse(SuccessResponse):
    data: CalendarPlan


class CalendarPlanListData(ListData):
    items: List[CalendarPlan]


class CalendarPlanListSuccessResponse(SuccessResponse):
    data: CalendarPlanListData


class NewCalendarPlan(BaseModel):
    day_of: date
    day_plan_id: int