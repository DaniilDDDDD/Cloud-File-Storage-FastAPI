import ormar

from database import MainMeta
from users.models import User


class File(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    author: User = ormar.ForeignKey(User, nullable=True)
    access: str = ormar.String(max_length=50, nullable=False)
    download_count: int = ormar.BigInteger(nullable=False)
    file: str = ormar.String(max_length=1000)
