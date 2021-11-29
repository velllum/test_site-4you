import asyncio
import logging
from fastapi import FastAPI

from .models.base import ErrorResponse


logger = logging.getLogger(__name__)


def create_app():
    """- точка входа"""
    app = FastAPI(
        title="USER HTTP REST API",
        responses=responses(),
        debug=True,
    )

    app.state.loop = asyncio.get_event_loop()
    register_config(app)
    register_startup(app)
    # register_routers(app)

    return app


def register_startup(app):
    """- запускается в начале работы"""
    print("* START")

    @app.on_event("startup")
    async def handler():
        register_database(app)


def register_config(app):
    """- регистрируем конфигурационные файлы"""
    print("* CONFIG")
    from . import config
    app.state.config = config.settings.settings


def register_database(app):
    """- регистрируем ьподключение к базе данных"""
    print("* DATABASE")
    from . import database as db
    app.state.db = db.get_session(app)


def register_routers(app):
    """- добавляем роуты"""
    print("* ROUTERS")
    from . import routers
    routers.register_routers(app)


def responses():
    """- реализуем ответы ошибок"""
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
