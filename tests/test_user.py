from application.database.db import get_db, get_session
from application.models.users import User
from application.schemas.users import CreateUser

# data_user = dict(
#         name="Name",
#         surname="Surname",
#         middle_name="Middle name",
#         email="email@email.ru",
#         password="00000aaaa"
#     )


def test_users(client, prefix):
    """- проверка всех пользователей"""
    with client.get(prefix) as response:
        assert response.status_code == 200
        assert isinstance(response.json(), list) is True


def test_search(client, prefix, user):
    """- проверка поиска"""
    with client.get(f"{prefix}/search/", params=dict(q=user["name"])) as response:
        response_user = response.json()
        assert response.status_code == 200
        assert response_user[0]["id"] == user["id"]


def test_user(client, prefix, user):
    """- проверка пользователя"""
    with client.get(f"{prefix}/{user['id']}/") as response:
        response_user = response.json()
        assert response.status_code == 200
        assert response_user["id"] == user["id"]


def test_user_create(client, prefix, app, data_user: CreateUser):
    """- проверка создания пользователя"""
    session = app.state.db

    with client.post(f"{prefix}/create", data=data_user.json()) as response:
        assert response.status_code == 200
        user = session.query(User).filter(User.email == data_user.email).first()
        assert user.email == data_user.email


# def test_user_delete(client, prefix, user):
#     """- проверка удаления пользователя"""
#     with client.delete(f"{prefix}/{user['id']}/") as response:
#         # response_user = response.json()
#         assert response.status_code == 307
#         assert response.is_redirect
#         assert response.reason is False

