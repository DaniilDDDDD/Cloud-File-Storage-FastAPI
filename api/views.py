import ormar
from typing import List
from fastapi import APIRouter, Depends, File as _File, UploadFile, BackgroundTasks

from users.models import User
from users.routers import current_user

from .models import File
from .schemas import FileListSchema, FileCreateSchema
from .utils import save_file

router = APIRouter(prefix='/files')


@router.get('/', response_model=List[FileListSchema])
async def list_logined(user: User = Depends(current_user)):
    files = await File.objects.filter(
        ormar.or_(access='public', author=user)
    ).all()
    return files


@router.get('/public/', response_model=List[FileListSchema])
async def list_public():
    files = await File.objects.all()
    return files


@router.post('/', response_model=FileCreateSchema)
async def create(
        background_tasks: BackgroundTasks,
        user: User = Depends(current_user),
        file: UploadFile = _File(...),
        access: str = 'only_author'
):
    file = await save_file(
        file=file,
        author=user,
        access=access,
        download_count=0,
        background_tasks=background_tasks
    )
    return {
        'id': file.id,
        'author': str(user.id),
        'access': access,
        'download_count': 0,
        'file': file.file
    }
