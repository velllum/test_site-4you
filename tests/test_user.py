from .conftest import get_user


def test_user_create(client, prefix, db, data_user):
    """- проверка создания пользователя"""
    with client.post(f"{prefix}/create", data=data_user.json()) as response:
        assert response.status_code == 200
        user = get_user(db, data_user)
        assert user.email == data_user.email


def test_users(client, prefix):
    """- проверка всех пользователей"""
    with client.get(prefix) as response:
        assert response.status_code == 200
        assert isinstance(response.json(), list) is True


def test_search(client, prefix, data_user):
    """- проверка поиска"""
    with client.get(f"{prefix}/search/", params=dict(q=data_user.name)) as response:
        assert response.status_code == 200

        if response.text == "Ничего не найдено, попробуйте еще раз":
            assert isinstance(response.text, str) is True

        response_user = response.json()
        assert isinstance(response_user, list) is True
        assert len(response_user) > 0

        for user in response_user:
            assert data_user.name in user.values()


def test_user(client, prefix, user):
    """- проверка пользователя"""
    with client.get(f"{prefix}/{user.id}/") as response:
        response_user = response.json()
        assert response.status_code == 200
        assert response_user["id"] == user.id


def test_user_update(client, prefix, data_user, user):
    """- проверка обновления пользователя"""
    with client.put(f"{prefix}/{user.id}", data=data_user.json()) as response:
        response_user = response.json()
        assert response.status_code == 200
        assert response_user["created_date"] != user.created_date


def test_user_delete(client, prefix, user):
    """- проверка удаления пользователя"""
    with client.delete(f"{prefix}/{user.id}") as response:
        assert response.status_code == 200
        assert response.text == "Пользователь был удален"
