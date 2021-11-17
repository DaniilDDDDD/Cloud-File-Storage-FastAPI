from typing import Optional
import ormar
from pydantic import EmailStr

from database import MainMeta


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=250, nullable=False)
    email: EmailStr = ormar.String(max_length=250, nullable=False)
    first_name: Optional[str] = ormar.String(max_length=250, nullable=True)
    last_name: Optional[str] = ormar.String(max_length=250, nullable=True)
    password: str = ormar.String(max_length=1000, nullable=False)
