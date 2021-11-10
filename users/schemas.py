from typing import Optional
from fastapi_users import models
from pydantic import BaseModel, EmailStr


class User(models.BaseUser):
    first_name: Optional[str]
    last_name: Optional[str]


class UserCreate(models.BaseUserCreate):
    # is_active: Optional[bool] = None
    # is_superuser: Optional[bool] = None
    # is_verified: Optional[bool] = None
    first_name: Optional[str]
    last_name: Optional[str]


class UserUpdate(models.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]


class UserDB(User, models.BaseUserDB):
    pass


class UserListSchema(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
