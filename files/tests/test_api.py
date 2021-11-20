import pytest

from .client import FilesClient

from files.models import File
from users.models import User


# @pytest.fixture
# async def create_files():
#     file_public = await File.create_file(
#
#     )