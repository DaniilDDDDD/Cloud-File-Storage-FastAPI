import pathlib
import asyncio

import pytest

from .client import FilesClient

from users.models import User
from users.auth import create_token

from ..models import File


@pytest.fixture()
async def get_test_user() -> User:
    yield await User.objects.get_or_create(
        username='test.user',
        email='user@test.com',
        password=User.get_hashed_password('qwerty1234')
    )


@pytest.fixture()
async def get_test_user_token(get_test_user) -> str:
    yield create_token(
        get_test_user.username
    )['access_token']


# @pytest.mark.asyncio
def test_files(get_test_user, get_test_user_token):

    client = FilesClient()

    # create

    response = client.create(
        'public',
        f'{pathlib.Path(__file__).parent.absolute()}/test_files/test_file_1.txt',
        get_test_user_token
    )
    assert response.status_code == 200
    response = response.json()
    assert 'id' in response
    assert 'file' in response
    assert response['access'] == 'public'
    assert response['download_count'] == 0
    public_file = {
        'id': response['id'],
        'file': response['file']
    }

    response = client.create(
        'private',
        f'{pathlib.Path(__file__).parent.absolute()}/test_files/test_file_2.txt',
        get_test_user_token
    )
    assert response.status_code == 200
    response = response.json()
    assert 'id' in response
    assert 'file' in response
    assert response['access'] == 'private'
    assert response['download_count'] == 0
    private_file = {
        'id': response['id'],
        'file': response['file']
    }

    # list
    response = client.list_public()
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 1
    assert response[0]['author'] == get_test_user.id
    assert response[0]['id'] == public_file['id']
    assert response[0]['file'] == public_file['file']

    response = client.list(get_test_user_token)
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 2
    for item in response:
        if item['access'] == 'public':
            assert item['author'] == get_test_user.id
            assert item['id'] == public_file['id']
            assert item['file'] == public_file['file']

        if item['access'] == 'private':
            assert item['author'] == get_test_user.id
            assert item['id'] == private_file['id']
            assert item['file'] == private_file['file']

    # task = asyncio.create_task(File.objects.all())
    # files = await task
    #
    # for file in files:
    #     if file.access == 'public':
    #         assert file.author == get_test_user
    #         assert file.id == public_file['id']
    #         assert file.file == public_file['file']
    #
    #     if file.access == 'public':
    #         assert file.author == get_test_user
    #         assert file.id == private_file['id']
    #         assert file.file == private_file['file']

    # retrieve
    response = client.retrieve_public(public_file['id'])
    assert response.status_code == 200
    response = response.json()
    assert 'view_link' in response
    assert 'download_link' in response
    public_file['view_link'] = response['view_link']
    public_file['download_link'] = response['download_link']

    response = client.retrieve_public(private_file['id'])
    assert response.status_code == 404

    response = client.retrieve(private_file['id'], get_test_user_token)
    assert response.status_code == 200
    response = response.json()
    assert 'view_link' in response
    assert 'download_link' in response
    private_file['view_link'] = response['view_link']
    private_file['download_link'] = response['download_link']

    # view
    response = client.get(public_file['view_link'])
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    assert response.content.decode('utf-8') == 'Test file public!'

    response = client.get(private_file['view_link'])
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    assert response.content.decode('utf-8') == 'Test file private!'

    # download
    response = client.get(public_file['download_link'])
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    assert 'attachment' in response.headers['content-disposition']

    response = client.get(private_file['download_link'])
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    assert 'attachment' in response.headers['content-disposition']

    # update
    response = client.update(
        public_file['id'],
        'private',
        get_test_user_token
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == public_file['id']
    assert response['access'] == 'private'
    # task = asyncio.create_task(File.objects.get(pk=public_file['id']))
    # file = await task
    # assert file.access == 'private'

    response = client.update(
        private_file['id'],
        'public',
        get_test_user_token
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == private_file['id']
    assert response['access'] == 'public'
    # task = asyncio.create_task(File.objects.get(pk=private_file['id']))
    # file = await task
    # assert file.access == 'public'

    # delete
    response = client.delete_file(public_file['id'], get_test_user_token)
    assert response.status_code == 204
    # task = asyncio.create_task(File.objects.get_file(pk=public_file['id']))
    # file = await task
    # assert not file

    response = client.list(get_test_user_token)
    assert len(response.json()) == 1

    response = client.delete_file(private_file['id'], get_test_user_token)
    assert response.status_code == 204
    # task = asyncio.create_task(File.objects.get_file(pk=private_file['id']))
    # file = await task
    # assert not file

    response = client.list(get_test_user_token)
    assert len(response.json()) == 0
