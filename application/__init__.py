import logging
from fastapi import FastAPI
import asyncio
from models.base import ErrorResponse


logger = logging.getLogger(__name__)


def create_app():
    """- точка входа"""
    root_path = config.get('root_path', None)
    app = FastAPI(
        title="CraftRadio HTTP REST API",
        debug=True,
        root_path=root_path,
    )

    app.state.args = args
    app.state.config = config

    register_startup(app)

    register_routers(app)

    logger.info(f"REST API app allocated")
    return app


def register_startup(app):
    """- запускается в начале работы"""
    @app.on_event("startup")
    async def handler():
        await startup(app)


def register_routers(app):
    """- добавляем роуты"""
    from . import routers
    return routers.register_routers(app)


async def startup(app):
    """- инициализируем данные на старте"""
    app.state.loop = asyncio.get_event_loop()

    app.state.db_pool = await db.init(app.state.config['db'])
    app.state.redis_pool = await redis.init(app.state.config['redis'])
    app.state.smtp = await smtp.init(app.state.config['smtp'])
    await storage.init(app.state.config['storage'])

    return app


def responses():
    return {
        400: {
            "model": ErrorResponse
        },
        401: {
            "model": ErrorResponse
        },
        404: {
            "model": ErrorResponse
        },
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    }
