from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from .utils import get_user_by_username, verify_password

ALGORITHM = "HS256"
access_token_jwt_subject = "access"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "Sdasdad3w#RmF34ef43%E5&*6DV%$5DSvBF*fY9V(y*&VNFdfBU(t8DnfDS"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_token(username: str) -> dict:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"username": username}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        username = decode_token(token).get('username')
        if not username:
            raise credentials_error
        user = await get_user_by_username(username)
        if not user:
            raise credentials_error
        return user
    except JWTError:
        raise credentials_error


async def get_current_user_or_none(token: str = Depends(oauth2_scheme)):
    try:
        username = decode_token(token).get('username')
        if not username:
            raise credentials_error
        user = await get_user_by_username(username)
        if not user:
            raise credentials_error
        return user
    except JWTError:
        return None


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
