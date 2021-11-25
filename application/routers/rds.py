import re
from typing import List
from models.base import (
    SuccessResponse
)

from models.rds import (
    Rds,
    RdsSuccessResponse,
    RdsType,
    AnimationConf
)
from pydantic.error_wrappers import ValidationError
from fastapi import (
    APIRouter,
    Request,
    Depends
)
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.session import get as get_session
from misc.session import Session
from misc.db import Connection
from misc.handlers import error_404, error_400_with_detail, error_400
from db import rds as db_rds

router = APIRouter(
    tags=['rds']
)


@router.get("/{radio_id}/rds", response_model=SuccessResponse)
async def get(
    radio_id: int,
    conn: Connection = Depends(get_db)
):
    result = await db_rds.get(conn, radio_id)
    #if not result:
    #    return await error_404("RDS doesn't exist or was deleted")
    return SuccessResponse(data=result)


@router.post("/{radio_id}/rds", response_model=RdsSuccessResponse)
async def update(
    radio_id: int,
    rds: Rds = Rds(),
    conn: Connection = Depends(get_db),
    session: Session = Depends(get_session)
):
    if not rds_valid(rds):
        return await error_400_with_detail("Rds is not valid")

    if rds.type == RdsType.ANIMATE_PS:
        if not animate_ps_valid(rds.animate_ps):
            return await error_400()
        rds.animate_ps['anim_construct'] = [string.strip() for string in rds.animate_ps['anim_construct']]

    result = await db_rds.update(conn, radio_id, rds)
    return RdsSuccessResponse(data=result)


@router.delete("/{radio_id}/rds", response_model=SuccessResponse)
async def delete(
        radio_id: int,
        conn: Connection = Depends(get_db),
        session: Session = Depends(get_session)
):
    rds = await db_rds.get(conn, radio_id)
    if rds == {}:
        return await error_404("RDS is empty")

    result = await db_rds.delete(conn, radio_id)
    return SuccessResponse(data=result)


def rds_valid(rds: Rds) -> bool:
    if pi_check(rds.pi) and bf_af_check(rds.bf, rds.af):
        return True
    return False


def pi_check(pi: str) -> bool:
    return True if re.match(r'[A-Fa-f0-9]{4}', pi) and len(pi) == 4 else False


def bf_af_check(bf: float, af: List[float]) -> bool:
    for elem in af+[bf]:
        elem = round(elem, 1)
        if not (87.5 <= elem <= 108.0):
            return False
    return True


def animate_ps_valid(anim_conf: dict) -> bool:
    try:
        anim_conf = AnimationConf(**anim_conf)
    except ValidationError:
        return False
    if not animate_ps_check(anim_conf):
        return False
    return True


def animate_ps_check(animate_ps: AnimationConf) -> bool:
    if len(animate_ps.anim_construct) <= 32 and (1 <= animate_ps.interval <= 16):
        for elem in animate_ps.anim_construct:
            if len(elem.strip()) > 64:
                return False
        return True
    return False


