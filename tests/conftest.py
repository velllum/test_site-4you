from typing import Dict

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from application import create_app
from application.schemas.users import CreateUser


@pytest.fixture
def data_user():
    """- Временные данные тестового пользователя"""
    data = dict(
        name="Name",
        surname="Surname",
        middle_name="Middle name",
        email="email@email.ru",
        password="00000aaaa"
    )

    yield CreateUser(**data)


@pytest.fixture
def app() -> FastAPI:
    """- получить объект приложения"""
    app = create_app()
    yield app


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
def user(client: TestClient, prefix: str) -> Dict:
    """- получить клиента"""
    response = client.get(prefix).json()
    if response:
        yield response[0]
