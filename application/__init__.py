import logging
from fastapi import FastAPI

from application.schemas.base import ErrorResponse


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- инициализация приложения"""
    app = FastAPI(
        title="USER HTTP REST API",
        debug=True,
    )

    register_config(app)
    register_startup(app)
    register_shutdown(app)
    register_routers(app)

    return app


def register_startup(app: FastAPI):
    """- запускается в начале работы"""
    logger.info("* START")

    @app.on_event("startup")
    async def handler():
        try:
            await register_database(app)
            logger.info(f"REST API app startup executed")
        except Exception as e:
            logger.exception(e, 'Startup crashed')


def register_shutdown(app: FastAPI):
    """- запускается в конце"""
    logger.info("* SHUTDOWN")

    @app.on_event("shutdown")
    async def handler():
        logger.info('Shutdown called')
        try:
            await close_database(app)
        except Exception as e:
            logger.exception(e, 'Shutdown crashed')


def register_config(app: FastAPI):
    """- регистрируем конфигурационные файлы"""
    logger.info("* CONFIG")
    from application.config.settings import settings
    app.state.config = settings


# ==========================================


async def register_database(app: FastAPI):
    """- регистрируем подключение к базе данных"""
    logger.info("* START DATABASE")
    from application.database import db
    app.state.db = db.get_db()


async def close_database(app):
    """- закрываем базу данных"""
    logger.info("* CLOSE DATABASE")
    db = app.state.db
    if db:
        db.close()

# ==========================================


def register_routers(app: FastAPI):
    """- добавляем роуты"""
    logger.info("* ROUTERS")
    from application import routers
    routers.get_routers(app)
