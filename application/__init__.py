import logging
from fastapi import FastAPI


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- создаем приложение"""
    app = FastAPI(
        title="USER HTTP REST API",
        debug=True,
    )

    init(app)

    return app


def init(app: FastAPI):
    """- инициализируем пакеты"""
    register_config(app)
    register_startup(app)
    register_shutdown(app)
    register_routers(app)


def register_startup(app: FastAPI):
    """- запускается в начале работы"""
    @app.on_event("startup")
    async def handler():
        try:
            await start_database(app)
            logger.info("Запуск выполнен")
        except Exception as e:
            logger.exception(e, 'Сбой при запуске')


def register_shutdown(app: FastAPI):
    """- запускается в конце"""
    @app.on_event("shutdown")
    async def handler():
        logger.info('Завершение работы')
        try:
            await close_database(app)
        except Exception as e:
            logger.exception(e, 'Сбой при выключении')


def register_config(app: FastAPI):
    """- регистрируем конфигурационные файлы"""
    logger.info("Запуск конфигурационных файлов")
    from .config.settings import settings
    app.state.config = settings


async def start_database(app: FastAPI):
    """- регистрируем подключение к базе данных"""
    logger.info("Запуск базы данных")
    from .database import db
    app.state.db = db.get_session()


async def close_database(app):
    """- закрываем базу данных"""
    logger.info("Закрыть базу данных")
    db = app.state.db
    if db:
        db.close()


def register_routers(app: FastAPI):
    """- добавляем представлений"""
    logger.info("Запуск представлений")
    from . import routers
    routers.get_routers(app)
