from core.database import metadata
from core.main import app

from .database import engine, database

metadata.create_all(engine)

app.state.database = database
