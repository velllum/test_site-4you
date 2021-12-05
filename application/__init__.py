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
    register_routers(app)


def register_config(app: FastAPI):
    """- регистрируем конфигурационные файлы"""
    logger.info("Запуск конфигурационных файлов")
    from .config.settings import settings
    app.state.config = settings


def register_routers(app: FastAPI):
    """- добавляем представлений"""
    logger.info("Запуск представлений")
    from . import routers
    routers.get_routers(app)
