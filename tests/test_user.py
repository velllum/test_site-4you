

def test_users(client, prefix):
    """- проверка списка юзеров"""
    with client.get(prefix) as response:
        assert response.status_code == 200
        assert isinstance(response.json(), list) is True


def test_search(client, prefix, user_name):
    """- проверка поиска"""
    with client.get(f"{prefix}/search/", params=dict(q=user_name)) as response:
        assert response.status_code == 200
