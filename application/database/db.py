import logging
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from ..config.settings import settings as st


logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    # получить подключение
    en = create_engine(
        url=st.db,
        connect_args={'check_same_thread': False},
    )
    return en


engine = get_engine()


def get_session() -> Session:
    """- создаем сессию"""
    sess = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )
    return sess()


def get_db() -> Optional[Session]:
    """- получить сессию подключения к базе данных"""
    session = get_session()
    try:
        yield session
    finally:
        session.close()
