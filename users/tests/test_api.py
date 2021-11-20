import pytest

from .client import UserClient
from ..schemas import UserCreateSchema


@pytest.fixture
def get_random_user():
    return UserCreateSchema(
        username='test_user',
        email='user@test.com',
        password='qwerty1234'
    )


@pytest.mark.asyncio
def test_register_and_login(get_random_user):
    client = UserClient()

    response = await client.register(get_random_user)
    assert response.status_code == 200
    assert 'id' in response.json()

    response = await client.register(get_random_user)
    assert response.status_code == 400

    response = await client.login(get_random_user)
    assert response.status_code == 200
    assert 'access_token' in response.json()
