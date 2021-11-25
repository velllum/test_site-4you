from misc import db
from fastapi import APIRouter, Request, Depends
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.db import Connection
from db import hour_plans as db_hour_plans
from models.hour_plans import (
    HourPlan,
    HourPlanListData,
    HourPlanListSuccessResponse,
    HourPlanSuccessResponse,
    NewHourPlan
)
from misc.handlers import (
    error_404,
    error_400_with_detail
)
from .blocks import add_block_secure_links


router = APIRouter(
    tags=['hour_plans']
)


@router.post("/{radio_id}/hour_plans", response_model=HourPlanSuccessResponse)
async def create(
    request: Request,
    radio_id: int,
    hour_plan: NewHourPlan,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_hour_plans.create(conn, radio_id, hour_plan)
    return HourPlanSuccessResponse(data=add_hour_plan_secure_links(request, conf, result))


@router.get("/{radio_id}/hour_plans/all", response_model=HourPlanListSuccessResponse)
async def get_list(
    request: Request,
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_hour_plans.get_list(conn, radio_id)
    return HourPlanListSuccessResponse(
        data=HourPlanListData(
            total=len(result),
            limit=len(result),
            page=1,
            items=[add_hour_plan_secure_links(request, conf, i) for i in result]
        )
    )


@router.post("/{radio_id}/hour_plans/{pk}", response_model=HourPlanSuccessResponse)
async def update(
    request: Request,
    radio_id: int,
    pk: int,
    hour_plan: NewHourPlan,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_hour_plans.update(conn, pk, hour_plan)
    return HourPlanSuccessResponse(data=add_hour_plan_secure_links(request, conf, result))


@router.delete("/{radio_id}/hour_plans/{pk}", response_model=HourPlanSuccessResponse)
async def delete(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    if await db_hour_plans.is_default(conn, pk):
        return await error_400_with_detail(detail='Default hour plan cant be removed')

    result = await db_hour_plans.disable(conn, pk)
    return HourPlanSuccessResponse(data=add_hour_plan_secure_links(request, conf, result))


@router.post("/{radio_id}/hour_plans/{pk}/copy", response_model=HourPlanSuccessResponse)
async def copy(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_hour_plans.copy(conn, pk)
    return HourPlanSuccessResponse(data=add_hour_plan_secure_links(request, conf, result))


@router.get("/{radio_id}/hour_plans/{pk}", response_model=HourPlanSuccessResponse)
async def get(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_hour_plans.get(conn, pk)
    return HourPlanSuccessResponse(data=add_hour_plan_secure_links(request, conf, result))


@router.post("/{radio_id}/hour_plans/{pk}/set_default", response_model=HourPlanSuccessResponse)
async def set_default(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_hour_plans.get(conn, pk)

    if not result:
        return await error_404()

    if not result.is_default:
        result = await db_hour_plans.set_default(conn, radio_id, pk)
    return HourPlanSuccessResponse(data=add_hour_plan_secure_links(request, conf, result))


def add_hour_plan_secure_links(request: Request, conf: dict, item: HourPlan) -> HourPlan:
    item.blocks = [add_block_secure_links(request, conf, i) for i in item.blocks]
    return item