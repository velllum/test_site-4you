from fastapi import (
    APIRouter, 
    Request, 
    Depends
)
from models.radios import (
    Radio,
    RadioSuccessResponse,
    RadioListSuccessResponse,
    RadioListData,
    NewStreamRadio,
    NewPresetRadio,
    NewUrlsRadio,
    NewRadio,
    UpdateRadio
)
from models.user_radios import (
    Role
)
from misc.fastapi.depends.db import get as get_db
from misc.db import Connection as DbConnection
from misc.fastapi.depends.session import (
    get as get_session,
    Session
)
from db import (
    radios as db_radios,
    streams as db_streams
)
from misc.fastapi.depends.auth import (
    ANY_RELATED,
    ONWER_ONLY
)
from misc.handlers import (
    error_400
)


router = APIRouter(
    prefix="/radios",
    tags=['radios']
)


@router.get("/all", response_model=RadioListSuccessResponse)
async def get_list(
    conn: DbConnection = Depends(get_db),
    session: Session = Depends(get_session)
):
    result = await db_radios.get_list_by_user(conn, session.user.id)
    total = len(result)
    return RadioListSuccessResponse(
        data=RadioListData(total=total, page=1, limit=total, items=result)
    )


@router.post("/create/from/stream", response_model=RadioSuccessResponse)
async def create_from_stream(
    radio: NewStreamRadio,
    conn: DbConnection = Depends(get_db),
    session: Session = Depends(get_session)
):
    if not await db_streams.exists(conn, radio.stream_id):
        return await error_400('Stream not found')

    result = await db_radios.create(conn, session.user.id, NewRadio.parse_obj(radio))
    return RadioSuccessResponse(data=result)


@router.post("/create/from/preset", response_model=RadioSuccessResponse)
async def create_from_preset(
    radio: NewPresetRadio,
    conn: DbConnection = Depends(get_db),
    session: Session = Depends(get_session)
):
    preset = await db_radios.preset(conn, radio.preset_id)
    if not preset:
        return await error_400('Preset not found')

    result = await db_radios.create_from_preset(conn, session.user.id, radio, preset)
    
    return RadioSuccessResponse(data=result)


@router.post("/create/from/urls", response_model=RadioSuccessResponse)
async def create_from_urls(
    radio: NewUrlsRadio,
    conn: DbConnection = Depends(get_db),
    session: Session = Depends(get_session)
):
    result = await db_radios.create(conn, session.user.id, radio)
    return RadioSuccessResponse(data=result)


##
# Порядок определения адресов важен.
# 
# Сначала идет /presets за ним /{radio_id}.
# При смене очередности проверка пути /preset происходит на radio_id: int. 
# Что приводит к падению обработки запроса с 422 статусом (неверные входные параметры запроса)
##
@router.get("/presets", response_model=RadioListSuccessResponse)
async def presets(
    conn: DbConnection = Depends(get_db)
):
    result = await db_radios.presets(conn)
    total = len(result)
    return RadioListSuccessResponse(
        data=RadioListData(total=total, page=1, limit=total, items=result)
    )


@router.get("/{radio_id}", response_model=RadioSuccessResponse, dependencies=[ANY_RELATED])
async def get(
    radio_id: int,
    conn: DbConnection = Depends(get_db)
):
    result = await db_radios.get(conn, radio_id)
    return RadioSuccessResponse(data=result)


@router.post("/{radio_id}", response_model=RadioSuccessResponse, dependencies=[ONWER_ONLY])
async def update(
    radio_id: int,
    radio: UpdateRadio,
    conn: DbConnection = Depends(get_db)
):
    result = await db_radios.update(conn, radio_id, radio)
    return RadioSuccessResponse(data=result)