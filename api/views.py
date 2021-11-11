import os
import ormar
from typing import List
from fastapi import (
    APIRouter, Depends, File as _File,
    UploadFile, BackgroundTasks, HTTPException,
    Request, Form
)
from starlette.responses import FileResponse as DownloadResponse
from fastapi.responses import Response, FileResponse

from users.models import User
from users.routers import current_user

from .models import File
from .schemas import FileListSchema
from .utils import save_file

router = APIRouter(prefix='/files')


@router.get('/', response_model=List[FileListSchema])
async def list(user: User = Depends(current_user)):
    """
    Only for authenticated users. Returns list of public or yours files.
    """
    files = await File.objects.filter(
        ormar.or_(access='public', author=str(user.id))
    ).order_by(
        'download_count'
    ).all()
    return files


@router.get('/{file_pk}/')
async def retrieve(
        file_pk: int,
        request: Request,
        user: User = Depends(current_user)
):
    """
    Only for authenticated users. Returns links on concrete public or your file.
    """
    file = await File.objects.get_or_none(id=file_pk)
    if file:
        if file.access == 'public' or str(file.author) == str(user.id):
            netloc = request.url.netloc
            filename = file.file.split('/')[-1].split('.')[0]
            return {
                'id': file.id,
                'view_link': f'http://{netloc}/api/files/{filename}/view/',
                'download_link': f'http://{netloc}/api/files/{filename}/download/'
            }
        else:
            raise HTTPException(
                status_code=403,
                detail='You do not have permissions to perform this action!'
            )
    else:
        raise HTTPException(status_code=404, detail='File does not exist!')


@router.get('/public/', response_model=List[FileListSchema])
async def list_public():
    """
    Returns list of public or yours files.
    """
    files = await File.objects.filter(
        access='public'
    ).order_by(
        'download_count'
    ).all()
    return files


@router.get('/public/{file_pk}/')
async def retrieve_public(
        file_pk: int,
        request: Request
):
    """
    Returns links on concrete public file.
    """
    file = await File.objects.get_or_none(id=file_pk)
    if file:
        if file.access == 'public':
            netloc = request.url.netloc
            filename = file.file.split('/')[-1].split('.')[0]
            return {
                'id': file.id,
                'view_link': f'http://{netloc}/api/files/{filename}/view/',
                'download_link': f'http://{netloc}/api/files/{filename}/download/'
            }
        else:
            raise HTTPException(
                status_code=403,
                detail='You do not have permissions to perform this action!'
            )
    else:
        raise HTTPException(status_code=404, detail='File does not exist!')


@router.post('/', response_model=FileListSchema)
async def create(
        background_tasks: BackgroundTasks,
        user: User = Depends(current_user),
        file: UploadFile = _File(...),
        access: str = Form('only_author')
):
    """
    Only for authenticated users. Creates new file.
    """
    file = await save_file(
        file=file,
        author=user,
        access=access,
        download_count=0,
        background_tasks=background_tasks
    )
    return file


@router.patch('/{file_pk}/', response_model=FileListSchema)
async def update(
        file_pk: int,
        access: str = Form('only_author'),
        user: User = Depends(current_user)
):
    """
    Only for authenticated users. Updates access of your file.
    """
    file = await File.objects.get_or_none(id=file_pk)
    if file:
        if str(file.author) == str(user.id):
            await file.update(access=access)
            return file
        else:
            raise HTTPException(
                status_code=403,
                detail='You do not have permissions to perform this action!'
            )
    else:
        raise HTTPException(status_code=404, detail='File does not exist!')


@router.delete('/{file_pk}/')
async def delete(
        file_pk: int,
        user: User = Depends(current_user)
):
    """
    Only for authenticated users. Deletes one of your files.
    """
    file = await File.objects.get_or_none(id=file_pk)
    if file:
        if str(file.author) == str(user.id):
            os.remove(file.file)
            await file.delete()
            return Response(status_code=204)
        else:
            raise HTTPException(
                status_code=403,
                detail='You do not have permissions to perform this action!')
    else:
        raise HTTPException(status_code=404, detail='File does not exist!')


@router.get('/{file_name}/view/', response_class=FileResponse)
async def view(file_name: str):
    """
    Allows you to view file.
    """
    file = await File.objects.get_or_none(file__contains=file_name)
    if file:
        return file.file
    else:
        raise HTTPException(status_code=404, detail='File does not exist!')


@router.get('/{file_name}/download/')
async def download(file_name: str):
    """
    Allows you to download file.
    """
    file = await File.objects.get_or_none(file__contains=file_name)
    if file:
        return DownloadResponse(file.file, filename=file.file.split('/')[-1])
    else:
        raise HTTPException(status_code=404, detail='File does not exist!')
