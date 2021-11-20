import os

from sqlalchemy import create_engine
import databases
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

database = databases.Database(TEST_DATABASE_URL)

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
