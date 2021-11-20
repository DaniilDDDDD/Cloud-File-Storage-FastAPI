import os

from flask import Flask
from flask_admin import Admin

from dotenv import load_dotenv

from .users import views as users_views
from .files import views as files_views

load_dotenv()


def admin_start():
    app = Flask(__name__)
    admin = Admin(app, name='Cloud File Storage', template_mode='bootstrap3')

    users_views.install(admin)
    files_views.install(admin)

    app.config.update(SECRET_KEY=os.environ.get('ADMIN_APP_SECRET_KEY'))
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    app.run(port=7501)



