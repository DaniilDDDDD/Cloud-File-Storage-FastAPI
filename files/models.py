import os
import ormar
import pathlib
import shutil
import uuid
from fastapi import UploadFile, BackgroundTasks

from core.database import MainMeta
from users.models import User

basedir = pathlib.Path(__file__).parent.parent.absolute()


class File(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    author: User = ormar.ForeignKey(User, nullable=True)
    access: str = ormar.String(max_length=50, nullable=False)
    download_count: int = ormar.BigInteger(nullable=False, default=0)
    file: str = ormar.String(max_length=1000)

    @classmethod
    async def create_file(
            cls,
            file: UploadFile,
            author: User,
            access: str,
            download_count: int,
            background_tasks: BackgroundTasks
    ):
        def write_file(author_id: str, file_name, _file: UploadFile):
            if not os.path.exists(f'media/{author_id}'):
                os.mkdir(f'media/{author_id}')
            with open(file_name, 'wb') as buffer:
                shutil.copyfileobj(_file.file, buffer)

        ext = file.filename.split('.')[-1]
        filename = f'media/{author.id}/{uuid.uuid4().hex}.{ext}'
        background_tasks.add_task(write_file, author.id, filename, file)
        return await cls.objects.create(
            author=author,
            access=access,
            file=filename,
            download_count=download_count
        )

    @classmethod
    async def get_public_files(cls):
        return await cls.objects.filter(
            access='public'
        ).order_by(
            'download_count'
        ).all()

    @classmethod
    async def get_user_files(cls, user: User):
        return await cls.objects.filter(
            ormar.or_(access='public', author=str(user.id))
        ).order_by(
            'download_count'
        ).all()

    @classmethod
    async def get_file_or_none_by_id(cls, _id: int):
        return await cls.objects.get_or_none(id=_id)

    @classmethod
    async def get_file_or_none_by_filename(cls, filename: str):
        return await cls.objects.get_or_none(file__contains=filename)
