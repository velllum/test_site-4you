import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.models.users import Base

logger = logging.getLogger(__name__)


def get_session(app: FastAPI):
    """- получить сессию подключения к базе данных"""
    session = init_db(app.state.config.db)
    try:
        logger.info("** GET SESSION DATABASE")
        return session
    finally:
        session.close()


def init_db(path: str):
    """- реализация подключения"""
    logger.info("** INIT SESSION DATABASE")

    # создаем подключение
    engine = create_engine(
        url=path,
        connect_args={'check_same_thread': False},
    )

    Base.metadata.create_all(engine)

    # создаем сессию
    session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    return session()
