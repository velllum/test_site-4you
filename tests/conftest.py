import pytest
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from application import create_app
from application.models.users import User
from application.schemas.users import CreateUser


@pytest.fixture
def data_user():
    """- Временные данные тестового пользователя"""
    yield CreateUser(**dict(
        name="Name",
        surname="Surname",
        middle_name="Middle name",
        email="email@email.ru",
        password="00000aaaa"
    ))


@pytest.fixture
def app() -> FastAPI:
    """- получить объект приложения"""
    yield create_app()


@pytest.fixture
def db(app: FastAPI) -> Session:
    """- получить сессию к базе данных"""
    db = app.state.db
    if db:
        yield db


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """- получить клиента"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def prefix() -> str:
    """- получить префикс ссылки"""
    yield "/api/v1/users"


@pytest.fixture
def user(db: Session, data_user: CreateUser) -> User:
    """- получить клиента"""
    user = get_user(db, data_user)
    if user:
        return user


def get_user(session: Session, data: CreateUser) -> User:
    """- получить юзера по email значению"""
    return session.query(User).filter(User.email == data.email).first()
