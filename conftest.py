import os

from sqlalchemy import create_engine
import databases
from dotenv import load_dotenv

from core.database import MainMeta
from core.main import app

load_dotenv()

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

database = databases.Database(TEST_DATABASE_URL)

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def pytest_configure():
    MainMeta.database = database
    MainMeta.metadata.create_all(engine)

    app.state.database = database


def pytest_unconfigure():
    os.remove(TEST_DATABASE_URL.split(':///')[-1])
