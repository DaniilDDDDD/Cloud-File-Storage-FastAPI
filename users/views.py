from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .auth import (
    authenticate_user, credentials_error,
    create_token,
)
from .schemas import UserCreateSchema, UserListSchema
from .models import User

router = APIRouter(prefix='/auth')


@router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise credentials_error
    return create_token(user.username)


@router.post('/register', response_model=UserListSchema)
async def register(
        data: UserCreateSchema
):
    return await User.create_user(**data.dict())
