from contextvars import copy_context
from urllib.parse import uses_fragment
from asyncpg.connection import connect
from fastapi.param_functions import Query
from starlette.responses import HTMLResponse, JSONResponse 
from misc import db
from models.streams import (
    StreamShortListSuccessResponse, 
    StreamShortListData
)
from models.base import ErrorResponse
from misc.db import Connection
from fastapi import (
    APIRouter, 
    Request, 
    Depends
)
from misc.fastapi.depends.db import get as get_db
from misc.db import Connection
from db import streams as db_streams


router = APIRouter(
    prefix="/streams",
    tags=['streams'],
)


@router.get("/all", response_model=StreamShortListSuccessResponse)
async def get_list(
    conn: Connection = Depends(get_db)
):
    result = await db_streams.get_list_short(conn)
    total = len(result)
    return StreamShortListSuccessResponse(
        data=StreamShortListData(total=total, page=1, limit=total, items=result)
    )