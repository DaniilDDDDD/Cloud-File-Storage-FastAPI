import pytest

from .client import UserClient
from ..schemas import UserCreateSchema


@pytest.fixture(scope='module')
def get_random_user():
    return UserCreateSchema(
        username='test_user_auth',
        email='user_auth@test.com',
        password='qwerty1234'
    )


def test_register_and_login(get_random_user):
    client = UserClient()

    response = client.register(get_random_user)
    assert response.status_code == 200
    assert 'id' in response.json()

    response = client.register(get_random_user)
    assert response.status_code == 400

    response = client.login(get_random_user)
    assert response.status_code == 200
    assert 'access_token' in response.json()
