from fastapi.testclient import TestClient

from tests.app import app
from ..schemas import UserCreateSchema


class UserClient(TestClient):

    def __init__(self, *args, **kwargs):
        self.path = 'http://localhost:8000/api/auth'
        kwargs['app'] = app
        super(UserClient, self).__init__(*args, **kwargs)

    def register(self, user: UserCreateSchema):
        return self.post(f'{self.path}/register', json=user.dict())

    def login(self, user: UserCreateSchema):
        return self.post(
            f'{self.path}/token',
            data={
                'username': user.username,
                'password': user.password
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
