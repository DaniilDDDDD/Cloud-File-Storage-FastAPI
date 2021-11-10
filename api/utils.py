import os
import pathlib
import shutil
import uuid
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
