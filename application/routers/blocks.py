from misc import db
from models.blocks import (
    Block,
    BlockSuccessResponse,
    BlockListData,
    BlockListSuccessResponse,
    NewBlock
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
from db import blocks as db_blocks
from misc.handlers import error_404
from .sections import add_section_secure_links


router = APIRouter(
    tags=['blocks']
)


@router.post("/{radio_id}/blocks", response_model=BlockSuccessResponse)
async def create(
    request: Request,
    radio_id: int,
    block: NewBlock,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_blocks.create(conn, radio_id, block)
    return BlockSuccessResponse(data=add_block_secure_links(request, conf, result))
    
    
@router.get(
    "/{radio_id}/blocks/all", 
    response_model=BlockListSuccessResponse
)
async def get_list(
    request: Request,
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_blocks.get_list_by_radio(conn, radio_id)
    total = len(result)
    return BlockListSuccessResponse(
        data=BlockListData(
            total=total, 
            limit=total, 
            page=1, 
            items=[add_block_secure_links(request, conf, i) for i in result]
        )
    )


@router.post("/{radio_id}/blocks/{pk}", response_model=BlockSuccessResponse)
async def update(
    request: Request,
    radio_id: int,
    pk: int,
    block: NewBlock,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
 ):
    result = await db_blocks.update(conn, pk, block)
    return BlockSuccessResponse(data=add_block_secure_links(request, conf, result))


@router.delete("/{radio_id}/blocks/{pk}", response_model=BlockSuccessResponse)
async def delete(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
 ):
    result = await db_blocks.disable(conn, pk)
    return BlockSuccessResponse(data=add_block_secure_links(request, conf, result))


@router.get("/{radio_id}/blocks/{pk}", response_model=BlockSuccessResponse)
async def get(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_blocks.get(conn, pk)
    return BlockSuccessResponse(data=add_block_secure_links(request, conf, result))


def add_block_secure_links(request: Request, conf: dict, item: Block) -> Block:
    item.sections = [add_section_secure_links(request, conf, i) for i in item.sections]
    return item
