from flask_admin.contrib.sqla import ModelView

from core.database import session
from core.models import File


class FileAdmin(ModelView):
    column_list = ('id', 'access', 'file', 'download_count')


def install(flask_admin):
    category_name = 'Files'

    flask_admin.add_views(
        FileAdmin(
            File,
            session,
            category=category_name
        )
    )
