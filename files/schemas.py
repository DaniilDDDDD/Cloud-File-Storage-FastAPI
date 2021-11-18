from pydantic import BaseModel, validator

from users.schemas import UserIdSchema


class FileListSchema(BaseModel):
    id: int
    author: UserIdSchema
    access: str
    download_count: int
    file: str

    @validator('author')
    def author_validator(cls, value):
        return int(value.id)
