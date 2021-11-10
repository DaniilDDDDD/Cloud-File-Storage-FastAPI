from pydantic import BaseModel

from users.schemas import UserListSchema


class FileListSchema(BaseModel):
    id: int
    author: UserListSchema
    access: str
    download_count: int
    file: str


class FileCreateSchema(BaseModel):
    id: int
    author: str
    access: str
    download_count: int
    file: str
