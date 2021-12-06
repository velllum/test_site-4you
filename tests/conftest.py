import pytest
from starlette.testclient import TestClient

from application import create_app


@pytest.fixture
def app():
    """- получить объект приложения"""
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """- получить клиента"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def prefix():
    """- получить префикс ссылки"""
    yield "/api/v1/users"


@pytest.fixture
def user_name(client, prefix):
    """- получить клиента"""
    response = client.get(prefix).json()
    if response:
        yield response[0]["name"]
