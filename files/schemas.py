from pydantic import BaseModel, validator

from users.schemas import UserListSchema


class FileListSchema(BaseModel):
    id: int
    author: UserListSchema
    access: str
    download_count: int
    file: str

    @validator('author')
    def author_validator(cls, value):
        return str(value.id)
