import databases
import ormar
import sqlalchemy


metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite:///sqlite.db")
engine = sqlalchemy.create_engine("sqlite:///sqlite.db")


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
