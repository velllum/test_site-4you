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
        tracks.router,
        prefix=API_PREFIX,
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
