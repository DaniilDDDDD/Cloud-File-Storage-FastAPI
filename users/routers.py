from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from .models import user_db
from .schemas import User, UserDB, UserCreate, UserUpdate
from .auth import auth_backends, jwt_authentication
from .views import on_after_register

users_router = APIRouter()

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB
)

users_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix='/auth/jwt',
    tags=['auth']
)
users_router.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix='/auth'
)
users_router.include_router(
    fastapi_users.get_users_router(),
    prefix='/users'
)

current_user = fastapi_users.current_user()
