from models.tracks import (
    Track, 
    NewTrack,
    TrackListData,
    TrackSuccessResponse,
    TrackListSuccessResponse
)
from misc import db
from fastapi import APIRouter, Request, Depends
from misc.db import Connection
from db import tracks as db_tracks
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.handlers import error_400_with_detail, error_404
from misc.lookup import (
    LookupDefinition,
    FieldDefinition as  FD
)
from models.base import (
    OperatorType,
    Lookup,
    Filter
)
from misc.storage import add_secure_url

router = APIRouter(
    tags=['tracks']
)

lookup_def = LookupDefinition(
    [
        FD('name', str, [OperatorType.ILIKE, OperatorType.EQ]),
        FD('rds_text', str, [OperatorType.ILIKE, OperatorType.EQ]),
        FD('play_rule', str, [OperatorType.EQ]),
        FD('group_pos', str, [OperatorType.EQ]),
        FD('category_id', int, [OperatorType.EQ]),

    ],
    default_order='name',
    orderable=['name'],
)


@router.post("/{radio_id}/tracks", response_model=TrackSuccessResponse)
async def create(
    request: Request,
    radio_id: int,
    track: NewTrack,
    conn: db.Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    if not await db_tracks.check_storages(conn, track.storage_ids):
        return await error_400_with_detail("Some storage_ids doesn't exist or was deleted")

    result = await db_tracks.create(conn, radio_id, track)
    return TrackSuccessResponse(data=add_track_secure_links(request, conf, result))


@router.get(
    "/{radio_id}/tracks/all",
    response_model=TrackListSuccessResponse,
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
    request: Request,
    radio_id: int,
    lookup: Lookup = Depends(lookup_def),
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
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

    result = await db_tracks.get_list(conn, lookup)
    total = await db.total_by_lookup(conn, "tracks", lookup)
    return TrackListSuccessResponse(
        data=TrackListData(
            total=total, 
            limit=lookup.limit, 
            page=lookup.page, 
            items=[add_track_secure_links(request, conf, i) for i in result]
        )
    )


@router.post("/{radio_id}/tracks/{pk}", response_model=TrackSuccessResponse)
async def update(
    request: Request,
    radio_id: int,
    pk: int,
    track: NewTrack,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    if not await db_tracks.select(conn, pk):
        return await error_400_with_detail("Track doesn't exist or was deleted")
    if not await db_tracks.check_storages(conn, track.storage_ids):
        return await error_400_with_detail("Some storage_ids doesn't exist or was deleted")
    result = await db_tracks.update(conn, radio_id, pk, track)
    return TrackSuccessResponse(data=add_track_secure_links(request, conf, result))


@router.delete("/{radio_id}/tracks/{pk}", response_model=TrackSuccessResponse)
async def delete(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    if not await db_tracks.select(conn, pk):
        return await error_400_with_detail("Track doesn't exist or was deleted")
    result = await db_tracks.delete(conn, pk)
    return TrackSuccessResponse(data=add_track_secure_links(request, conf, result))


@router.get("/{radio_id}/tracks/{pk}", response_model=TrackSuccessResponse)
async def get(
    request: Request,
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
):
    result = await db_tracks.select(conn, pk)
    if not result:
        return await error_404("Track doesn't exist or was deleted")
    return TrackSuccessResponse(data=add_track_secure_links(request, conf, result))


def add_track_secure_links(request: Request, conf: dict, item: Track) -> Track:
    item.storages = [
        add_secure_url(request, conf, i)
        for i in item.storages
    ]
    return item