from misc import db
from fastapi import APIRouter, Request, Depends
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.db import Connection
from db import day_plans as db_day_plans
from models.day_plans import (
    DayPlan,
    DayPlanListData,
    DayPlanSuccessResponse,
    DayPlanListSuccessResponse,
    NewDayPlan
)
from misc.handlers import (
    error_404,
    error_400_with_detail
)
from .hour_plans import add_hour_plan_secure_links


router = APIRouter(
    tags=['day_plans']
)


@router.post("/{radio_id}/day_plans", response_model=DayPlanSuccessResponse)
async def create(
    request: Request,
    radio_id: int,
    day_plan: NewDayPlan,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_day_plans.create(conn, radio_id, day_plan)
    return DayPlanSuccessResponse(data=add_day_plan_secure_links(request, conf, result))


@router.get("/{radio_id}/day_plans/all", response_model=DayPlanListSuccessResponse)
async def get_list(
    request: Request,
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_day_plans.get_list(conn, radio_id)
    return DayPlanListSuccessResponse(
        data=DayPlanListData(
            total=len(result),
            limit=len(result),
            page=1,
            items=[add_day_plan_secure_links(request, conf, i) for i in result]
        )
    )


@router.post("/{radio_id}/day_plans/{pk}", response_model=DayPlanSuccessResponse)
async def update(
    request: Request,
    radio_id: int,
    pk: int,
    day_plan: NewDayPlan,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_day_plans.update(conn, pk, day_plan)
    return DayPlanSuccessResponse(data=add_day_plan_secure_links(request, conf, result))


@router.delete("/{radio_id}/day_plans/{pk}", response_model=DayPlanSuccessResponse)
async def delete(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    if await db_day_plans.is_default(conn, pk):
        return await error_400_with_detail(detail='Default hour plan cant be removed')

    result = await db_day_plans.disable(conn, pk)
    return DayPlanSuccessResponse(data=add_day_plan_secure_links(request, conf, result))


@router.post("/{radio_id}/day_plans/{pk}/copy", response_model=DayPlanSuccessResponse)
async def copy(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_day_plans.copy(conn, pk)
    return DayPlanSuccessResponse(data=add_day_plan_secure_links(request, conf, result))


@router.get("/{radio_id}/day_plans/{pk}", response_model=DayPlanSuccessResponse)
async def get(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_day_plans.get(conn, pk)
    return DayPlanSuccessResponse(data=add_day_plan_secure_links(request, conf, result))


@router.post("/{radio_id}/day_plans/{pk}/set_default", response_model=DayPlanSuccessResponse)
async def set_default(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_day_plans.get(conn, pk)

    if not result:
        return await error_404()

    if not result.is_default:
        result = await db_day_plans.set_default(conn, radio_id, pk)
    return DayPlanSuccessResponse(data=add_day_plan_secure_links(request, conf, result))


def add_day_plan_secure_links(request: Request, conf: dict, item: DayPlan) -> DayPlan:
    item.hours = [add_hour_plan_secure_links(request, conf, i) if i else None for i in item.hours]
    return item