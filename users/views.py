from starlette.requests import Request

from .schemas import (
    UserDB
)


def on_after_register(user: UserDB, request: Request):
    pass
