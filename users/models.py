import ormar
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

from database import MainMeta
from users.schemas import UserDB


class User(OrmarBaseUserModel):
    class Meta(MainMeta):
        pass

    first_name = ormar.String(max_length=500, nullable=True)
    last_name = ormar.String(max_length=500, nullable=True)

    def __str__(self):
        return str(self.id)


user_db = OrmarUserDatabase(UserDB, User)
