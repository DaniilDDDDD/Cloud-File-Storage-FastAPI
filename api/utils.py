import os
import pathlib
import shutil
import uuid
import ormar
from fastapi import UploadFile, BackgroundTasks

from users.models import User
from .models import File

basedir = pathlib.Path(__file__).parent.parent.absolute()


async def save_file(
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
    return await File.objects.create(
        author=author.id,
        access=access,
        file=filename,
        download_count=download_count
    )


async def get_public_files():
    return await File.objects.filter(
        access='public'
    ).order_by(
        'download_count'
    ).all()


async def get_user_files(user):
    return await File.objects.filter(
        ormar.or_(access='public', author=str(user.id))
    ).order_by(
        'download_count'
    ).all()


async def get_file_or_none_by_id(_id: int):
    return await File.objects.get_or_none(id=_id)


async def get_file_or_none_by_filename(filename: str):
    return await File.objects.get_or_none(file__contains=filename)
