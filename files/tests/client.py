from fastapi.testclient import TestClient

from conftest import app
from users.models import User


class FilesClient(TestClient):
    def __init__(self, *args, **kwargs):
        self.path = 'http://localhost:8000/api/files'
        kwargs['app'] = app
        super(FilesClient, self).__init__(*args, **kwargs)

    def list_public(self):
        return self.get(f'{self.path}/public/')

    def retrieve_public(self, _id: int):
        return self.get(f'{self.path}/public/{_id}/')

    def list(self, token: str):
        return self.get(
            f'{self.path}/',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

    def retrieve(self, _id: int, token: str):
        return self.get(
            f'{self.path}/{_id}',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

    def create(self, access: str, file: str, token: str):
        return self.post(
            f'{self.path}/',
            data={'access': access},
            files={'file': open(file, 'rb')},
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

    def update(self, _id: int, access: str, token: str):
        return self.patch(
            f'{self.path}/{_id}/',
            data={
                'access': access
            },
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

    def delete_file(self, _id: int, token: str):
        return self.delete(
            f'{self.path}/{_id}/',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
