from fastapi import Depends
from misc.fastapi.depends.auth import (
    radio_relation_required,
    auth_required
)

from . import (
    users,
    auth,
    blocks,
    categories,
    tracks,
    calendar_plans,
    day_plans,
    hour_plans,
    sections,
    radios,
    streams,
    presets,
    storage,
    sound_templates,
    devices,
    rds
) 


VERSION_PREFIX = 'v2'
API_PREFIX = f'/api/{VERSION_PREFIX}'


def register_routers(app):    

    app.include_router(
        auth.router,
        prefix=API_PREFIX
    )

    app.include_router(
        storage.router,
        prefix=API_PREFIX
    )

    app.include_router(
        streams.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(auth_required)
        ]
    )
    
    app.include_router(
        radios.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(auth_required)
        ]
    )

    app.include_router(
        presets.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(auth_required)
        ]
    )

    app.include_router(
        tracks.router,
        prefix=API_PREFIX,
    )

    app.include_router(
        categories.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        sections.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        sound_templates.router,
        prefix=API_PREFIX,
    )

    app.include_router(
        calendar_plans.router,
        prefix=API_PREFIX,
    )

    app.include_router(
        day_plans.router,
        prefix=API_PREFIX,  
    )

    app.include_router(
        hour_plans.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )
    
    app.include_router(
        tracks.router,
        prefix=API_PREFIX,
    )

    app.include_router(
        calendar_plans.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        day_plans.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        hour_plans.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        sections.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        blocks.router,
        prefix=API_PREFIX,
        dependencies=[
            Depends(radio_relation_required())
        ]
    )

    app.include_router(
        devices.router,
        prefix=API_PREFIX,
    )

    app.include_router(
        rds.router,
        prefix=API_PREFIX,
    )

    return app