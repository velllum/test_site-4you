import logging
from fastapi import FastAPI

from application.schemas.base import ErrorResponse


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- точка входа"""
    app = FastAPI(
        title="USER HTTP REST API",
        responses=responses(),
        debug=True,
    )

    register_config(app)
    register_startup(app)
    register_shutdown(app)
    # register_routers(app)

    return app


def register_startup(app):
    """- запускается в начале работы"""
    logger.info("* START")

    @app.on_event("startup")
    async def handler():
        try:
            await register_database(app)
            logger.info(f"REST API app startup executed")
        except Exception as e:
            logger.exception(e, 'Startup crashed')


def register_shutdown(app):
    """- запускается в конце"""
    logger.info("* SHUTDOWN")

    @app.on_event("shutdown")
    async def handler():
        logger.info('Shutdown called')
        try:
            await close_database(app)
        except Exception as e:
            logger.exception(e, 'Shutdown crashed')


def register_config(app):
    """- регистрируем конфигурационные файлы"""
    logger.info("* CONFIG")
    from . import config
    app.state.config = config.settings.settings


async def register_database(app):
    """- регистрируем подключение к базе данных"""
    logger.info("* START DATABASE")
    from . import database as db
    app.state.db = db.get_session(app)


async def close_database(app):
    """- закрываем базу данных"""
    logger.info("* CLOSE DATABASE")
    if app.state.db:
        app.state.db.close()


def register_routers(app):
    """- добавляем роуты"""
    logger.info("* ROUTERS")
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
