from typing import Optional
import ormar
from pydantic import EmailStr
from passlib.context import CryptContext

from core.database import MainMeta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(
        primary_key=True)
    username: str = ormar.String(
        max_length=250, nullable=False, unique=True)
    email: EmailStr = ormar.String(
        max_length=250, nullable=False, unique=True)
    first_name: Optional[str] = ormar.String(
        max_length=250, nullable=True)
    last_name: Optional[str] = ormar.String(
        max_length=250, nullable=True)
    password: str = ormar.String(
        max_length=1000, nullable=True)

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def get_user_by_username(cls, username: str):
        return await cls.objects.get_or_none(username=username)

    @classmethod
    async def create_user(
            cls,
            username: str,
            email: str,
            password: str,
            first_name: str = None,
            last_name: str = None
    ):
        user = await User.objects.get_or_none(
            username=username,
            email=email
        )
        if not user:
            return await User.objects.create(
                username=username,
                email=email,
                password=cls.get_hashed_password(password),
                first_name=first_name,
                last_name=last_name
            )
        return None
