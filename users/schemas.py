from typing import Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    last_name: Optional[str]
    first_name: Optional[str]


class UserListSchema(UserSchema):
    id: int


class UserCreateSchema(UserSchema):
    password: str


class UserIdSchema(BaseModel):
    id: int
