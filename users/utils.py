from typing import Optional
from passlib.context import CryptContext

from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_username(username: str):
    return await User.objects.get_or_none(username=username)


async def create_user(
        username: str,
        email: str,
        password: str,
        first_name: Optional[str],
        last_name: Optional[str]
) -> User:
    return await User.objects.get_or_create(
        username=username,
        email=email,
        password=get_hashed_password(password),
        first_name=first_name,
        last_name=last_name
    )
