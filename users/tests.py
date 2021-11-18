import os
import asyncio
import sqlalchemy
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .views import router
from .models import User, MainMeta

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

app = FastAPI()
app.include_router(router)

engine = sqlalchemy.create_engine(DATABASE_URL)
MainMeta.metadata.create_all(engine)


async def get_test_user() -> User:
    return await User.objects.get_or_create(
        username='test.user',
        email='test@user.com',
        password=User.get_hashed_password('qwerty1234')
    )


async def delete_test_user(_user: User):
    await _user.delete()


def test_registration(_user: User):
    client = TestClient(app)

    response = client.post(
        'auth/register',
        data={
            'username': _user.username,
            'email': _user.email,
            'password': 'qwerty1234'
        }
    )
    assert response.status_code == 201


user = asyncio.run(get_test_user())
test_registration(user)
asyncio.run(delete_test_user(user))
