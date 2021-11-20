from fastapi.testclient import TestClient

from tests.app import app

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

    def list(self):
        return self.get(
            f'{self.path}/',
            headers={
                'Authorization': f'Bearer {User.get_test_user_token()}'
            }
        )

    def retrieve(self, _id: int):
        return self.get(
            f'{self.path}/{_id}',
            headers={
                'Authorization': f'Bearer {User.get_test_user_token()}'
            }
        )

    def create(self, data: dict):
        return self.post(
            f'{self.path}/',
            data={'access': data['access']},
            files={'file': open(data['file'], 'rb')},
            headers={
                'Authorization': f'Bearer {User.get_test_user_token()}'
            }
        )

    def update(self, _id: int, access: str):
        return self.patch(
            f'{self.path}/{_id}/',
            data={
                'access': access
            },
            headers={
                'Authorization': f'Bearer {User.get_test_user_token()}'
            }
        )

    def delete_file(self, _id: int):
        return self.delete(
            f'{self.path}/{_id}/',
            headers={
                'Authorization': f'Bearer {User.get_test_user_token()}'
            }
        )

    def view(self, filename: str):
        return self.get(f'{self.path}/{filename}/view/')

    def download(self, filename: str):
        return self.get(f'{self.path}/{filename}/download')
