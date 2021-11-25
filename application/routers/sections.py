from misc import db
from models.sections import (
    Section,
    SectionSuccessResponse,
    SectionListData,
    SectionListSuccessResponse,
    NewSection
)
from misc.db import Connection as DbConnection
from fastapi import (
    APIRouter, 
    Request, 
    Depends
)
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.db import Connection
from db import sections as db_sections
from misc.handlers import error_404
from .tracks import add_track_secure_links


router = APIRouter(
    tags=['sections']
)


@router.post("/{radio_id}/sections", response_model=SectionSuccessResponse)
async def create(
    request: Request,
    radio_id: int,
    category: NewSection,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_sections.create(conn, radio_id, category)
    return SectionSuccessResponse(data=add_section_secure_links(request, conf, result))
    
    
@router.get("/{radio_id}/sections/all", response_model=SectionListSuccessResponse)
async def get_list(
    request: Request,
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_sections.get_list_by_radio(conn, radio_id)
    total = len(result)
    return SectionListSuccessResponse(
        data=SectionListData(
            total=total, 
            limit=total, 
            page=1, 
            items=[add_section_secure_links(request, conf, i) for i in result]
        )
    )


@router.post("/{radio_id}/sections/{pk}", response_model=SectionSuccessResponse)
async def update(
    request: Request,
    radio_id: int,
    pk: int,
    category: NewSection,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
 ):
    result = await db_sections.update(conn, pk, category)
    return SectionSuccessResponse(data=add_section_secure_links(request, conf, result))


@router.delete("/{radio_id}/sections/{pk}", response_model=SectionSuccessResponse)
async def delete(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
 ):
    result = await db_sections.disable(conn, pk)
    return SectionSuccessResponse(data=add_section_secure_links(request, conf, result))
     

@router.post("/{radio_id}/sections/{pk}/copy", response_model=SectionSuccessResponse)
async def copy(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
 ):
    result = await db_sections.copy(conn, pk)
    return SectionSuccessResponse(data=add_section_secure_links(request, conf, result))


@router.get("/{radio_id}/sections/{pk}", response_model=SectionSuccessResponse)
async def get(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_sections.get_enabled(conn, pk)
    return SectionSuccessResponse(data=add_section_secure_links(request, conf, result))


def add_section_secure_links(request: Request, conf: dict, item: Section) -> Section:
    item.tracks_in = [add_track_secure_links(request, conf, i) for i in item.tracks_in]
    item.tracks_out = [add_track_secure_links(request, conf, i) for i in item.tracks_out]
    return item