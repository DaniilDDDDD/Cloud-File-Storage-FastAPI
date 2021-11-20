from flask_admin.contrib.sqla import ModelView

from core.database import session
from core.models import User


class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
    form_excluded_columns = ('password',)


def install(flask_admin):
    category_name = 'Users'

    flask_admin.add_views(
        UserAdmin(
            User,
            session,
            category=category_name
        )
    )
