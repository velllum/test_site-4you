from misc import db
from models.categories import (
    Category,
    CategorySuccessResponse,
    CategoryListData,
    CategoryListSuccessResponse,
    NewCategory
)
from misc.db import Connection as DbConnection
from fastapi import (
    APIRouter, 
    Request, 
    Depends
)
from misc.fastapi.depends.db import (
    get as get_db
)
from misc.db import Connection
from db import categories as db_categories
from misc.handlers import error_404
from misc.lookup import (
    LookupDefinition,
    FieldDefinition as  FD
)
from models.base import (
    Lookup,
    Filter,
    OperatorType
)


router = APIRouter(
    tags=['categories']
)


lookup_def = LookupDefinition(
    [
        FD('name', str, [OperatorType.ILIKE, OperatorType.EQ]),
    ],
    orderable=['name'],
    default_order='name',
    default_limit=None
)


@router.post("/{radio_id}/categories", response_model=CategorySuccessResponse)
async def create(
    radio_id: int,
    category: NewCategory,
    conn: Connection = Depends(get_db)
):
    result = await db_categories.create(conn, radio_id, category)
    return CategorySuccessResponse(data=result)
    
    
@router.get(
    "/{radio_id}/categories/all", 
    response_model=CategoryListSuccessResponse,
    openapi_extra=lookup_def.openapi_extra([{
        'in': 'path',
        'name': 'radio_id',
        'required': True,
        'schema': {
            'type': 'integer'
        }
    }])
)
async def get_list(
    radio_id: int,
    lookup: Lookup = Depends(lookup_def),
    conn: Connection = Depends(get_db)
):
    lookup.filters.append(
        Filter(
            field='radio_id',
            operator=OperatorType.EQ,
            value=radio_id
        )
    )
    lookup.filters.append(
        Filter(
            field='en',
            operator=OperatorType.EQ,
            value=True
        )
    )
    result = await db_categories.get_list_by_radio_and_lookup(conn, lookup)
    total = len(result)
    return CategoryListSuccessResponse(
        data=CategoryListData(total=total, limit=total, page=1, items=result)
    )


@router.post("/{radio_id}/categories/{pk}", response_model=CategorySuccessResponse)
async def update(
     radio_id: int,
     pk: int,
     category: NewCategory,
     conn: Connection = Depends(get_db)
 ):
    result = await db_categories.update(conn, pk, category)
    return CategorySuccessResponse(data=result)


@router.delete("/{radio_id}/categories/{pk}", response_model=CategorySuccessResponse)
async def delete(
     radio_id: int,
     pk: int,
     conn: Connection = Depends(get_db)
 ):
    result = await db_categories.disable(conn, pk)
    return CategorySuccessResponse(data=result)
     

@router.post("/{radio_id}/categories/{pk}/copy", response_model=CategorySuccessResponse)
async def copy(
     radio_id: int,
     pk: int,
     conn: Connection = Depends(get_db)
 ):
    result = await db_categories.copy(conn, pk)
    return CategorySuccessResponse(data=result)


@router.get("/{radio_id}/categories/{pk}", response_model=CategorySuccessResponse)
async def get(
     radio_id: int,
     pk: int,
     conn: Connection = Depends(get_db)
):
    result = await db_categories.get_enabled(conn, pk)
    return CategorySuccessResponse(data=result)
