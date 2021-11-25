from misc import db, session
from fastapi import APIRouter, Request, Depends
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.fastapi.depends.session import get as get_session
from misc.db import Connection
from db import calendar_plans as db_calendar_plans
from models.calendar_plans import (
    CalendarPlan,
    CalendarPlanListData,
    CalendarPlanSuccessResponse,
    CalendarPlanListSuccessResponse,
    NewCalendarPlan
)
from misc.handlers import (
    error_404,
    error_400_with_detail
)
from .day_plans import add_day_plan_secure_links


router = APIRouter(
    tags=['calendar_plans']
)


@router.post("/{radio_id}/calendar_plans", response_model=CalendarPlanSuccessResponse)
async def create(
    request: Request,
    radio_id: int,
    calendar_plan: NewCalendarPlan,
    session: session.Session = Depends(get_session),
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_calendar_plans.create(conn, radio_id, session.user.id, calendar_plan)
    return CalendarPlanSuccessResponse(data=add_calendar_plan_secure_links(request, conf, result))


@router.get("/{radio_id}/calendar_plans/all", response_model=CalendarPlanListSuccessResponse)
async def get_list(
    request: Request,
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_calendar_plans.get_list(conn, radio_id)
    return CalendarPlanListSuccessResponse(
        data=CalendarPlanListData(
            total=len(result),
            limit=len(result),
            page=1,
            items=[add_calendar_plan_secure_links(request, conf, i) for i in result]
        )
    )


@router.post("/{radio_id}/calendar_plans/{pk}", response_model=CalendarPlanSuccessResponse)
async def update(
    request: Request,
    radio_id: int,
    pk: int,
    calendar_plan: NewCalendarPlan,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_calendar_plans.update(conn, pk, calendar_plan)
    return CalendarPlanSuccessResponse(data=add_calendar_plan_secure_links(request, conf, result))


@router.delete("/{radio_id}/calendar_plans/{pk}", response_model=CalendarPlanSuccessResponse)
async def delete(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_calendar_plans.disable(conn, pk)
    return CalendarPlanSuccessResponse(data=add_calendar_plan_secure_links(request, conf, result))


@router.post("/{radio_id}/calendar_plans/{pk}/copy", response_model=CalendarPlanSuccessResponse)
async def copy(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_calendar_plans.copy(conn, pk)
    return CalendarPlanSuccessResponse(data=add_calendar_plan_secure_links(request, conf, result))


@router.get("/{radio_id}/calendar_plans/{pk}", response_model=CalendarPlanSuccessResponse)
async def get(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_calendar_plans.get(conn, pk)
    return CalendarPlanSuccessResponse(data=add_calendar_plan_secure_links(request, conf, result))


def add_calendar_plan_secure_links(request: Request, conf: dict, item: CalendarPlan) -> CalendarPlan:
    if item.day_plan:
        item.day_plan = add_day_plan_secure_links(request, conf, item.day_plan)
    return item