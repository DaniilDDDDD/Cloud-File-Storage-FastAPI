import os
from typing import List
from fastapi import (
    APIRouter, Depends, File as _File,
    UploadFile, BackgroundTasks, HTTPException,
    Request, Form
)
from starlette.responses import FileResponse as DownloadResponse
from fastapi.responses import Response, FileResponse

from users.models import User
from users.auth import get_current_user

from .schemas import FileListSchema
from .models import File

router = APIRouter(prefix='/files')


@router.get('/public/', response_model=List[FileListSchema])
async def list_public():
    """
    Returns list of public or yours files.
    """
    return await File.get_public_files()


@router.get('/public/{file_pk}/')
async def retrieve_public(
        file_pk: int,
        request: Request
):
    """
    Returns links on concrete public file.
    """
    file = await File.get_file_or_none_by_id(file_pk)
    if not file:
        raise HTTPException(
            status_code=403,
            detail='You do not have permissions to perform this action!'
        )
    if file.access == 'public':
        netloc = request.url.netloc
        filename = file.file.split('/')[-1].split('.')[0]
        return {
            'id': file.id,
            'view_link': f'http://{netloc}/api/files/{filename}/view/',
            'download_link': f'http://{netloc}/api/files/{filename}/download/'
        }
    raise HTTPException(status_code=404, detail='File does not exist!')


@router.get('/{file_name}/view/', response_class=FileResponse)
async def view(file_name: str):
    """
    Allows you to view file.
    """
    file = await File.get_file_or_none_by_filename(file_name)
    if not file:
        raise HTTPException(status_code=404, detail='File does not exist!')
    return file.file


@router.get('/{file_name}/download/')
async def download(file_name: str):
    """
    Allows you to download file.
    """
    file = await File.get_file_or_none_by_filename(file_name)
    if not file:
        raise HTTPException(status_code=404, detail='File does not exist!')
    await file.update(download_count=file.download_count + 1)
    return DownloadResponse(file.file, filename=file.file.split('/')[-1])


@router.get('/', response_model=List[FileListSchema])
async def list(user: User = Depends(get_current_user)):
    """
    Only for authenticated users.
    Returns list of public or yours files.
    """
    return await File.get_user_files(user)


@router.get('/{file_pk}/')
async def retrieve(
        file_pk: int,
        request: Request,
        user: User = Depends(get_current_user)
):
    """
    Only for authenticated users.
    Returns links on concrete public or your file.
    """
    file = await File.get_file_or_none_by_id(file_pk)
    if not file:
        raise HTTPException(status_code=404, detail='File does not exist!')

    if file.access == 'public' or str(file.author) == str(user.id):
        netloc = request.url.netloc
        filename = file.file.split('/')[-1].split('.')[0]
        return {
            'id': file.id,
            'view_link': f'http://{netloc}/api/files/{filename}/view/',
            'download_link': f'http://{netloc}/api/files/{filename}/download/'
        }
    raise HTTPException(
        status_code=403,
        detail='You do not have permissions to perform this action!'
    )


@router.post('/', response_model=FileListSchema)
async def create(
        background_tasks: BackgroundTasks,
        user: User = Depends(get_current_user),
        file: UploadFile = _File(...),
        access: str = Form('only_author')
):
    """
    Only for authenticated users. Creates new file.
    """
    file = await File.create_file(
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
        user: User = Depends(get_current_user)
):
    """
    Only for authenticated users. Updates access of your file.
    """
    file = await File.get_file_or_none_by_id(file_pk)
    if not file:
        raise HTTPException(status_code=404, detail='File does not exist!')

    if str(file.author) == str(user.id):
        return await file.update(access=access)

    raise HTTPException(
        status_code=403,
        detail='You do not have permissions to perform this action!'
    )


@router.delete('/{file_pk}/')
async def delete(
        file_pk: int,
        user: User = Depends(get_current_user)
):
    """
    Only for authenticated users. Deletes one of your files.
    """
    file = await File.get_file_or_none_by_id(file_pk)
    if not file:
        raise HTTPException(status_code=404, detail='File does not exist!')
    if str(file.author) == str(user.id):
        os.remove(file.file)
        await file.delete()
        return Response(status_code=204)
    raise HTTPException(
        status_code=403,
        detail='You do not have permissions to perform this action!')
