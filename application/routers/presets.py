from fastapi import (
    APIRouter, 
    Request, 
    Depends
)
from models.presets import (
    Preset,
    PresetListSuccessResponse,
    PresetListData
)
from misc.fastapi.depends.db import get as get_db
from misc.db import Connection as DbConnection
from misc.fastapi.depends.session import (
    get as get_session,
    Session
)
from db import (
    presets as db_presets
)



router = APIRouter(
    prefix="/presets",
    tags=['presets']
)



@router.get("/all", response_model=PresetListSuccessResponse)
async def get_list(
    conn: DbConnection = Depends(get_db)
):
    result = await db_presets.get_list_enabled(conn)
    return PresetListSuccessResponse(
        data=PresetListData(total=len(result), page=1, limit=len(result), items=result)
    )

