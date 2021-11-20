import os
import ormar
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)()


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
