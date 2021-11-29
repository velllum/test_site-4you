from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session(app: FastAPI):
    """- получить ссесию подключения к базе данных"""
    session = init_db(app.state.config.db)
    try:
        print("** SESSION DATABASE")
        yield session
    finally:
        session.close()


def init_db(path: str):
    """- реализация подключения"""

    # создаем подключение
    engine = create_engine(
        url=path,
        connect_args={'check_same_thread': False},
    )

    # создаем сессию
    session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    yield session()
