# Users module
Provides authentication system and ```User``` model.

## Usage
You need to do is to create python package ```core``` 
where will be ```database.py```:
```
#database.py

import os
import ormar
import databases
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
```
Also you need to have ```.env``` file with URL to your database. For example:
```
# .env

DATABASE_URL=sqlite:///sqlite.db
```

And finally you need to run ```metadata.create_all(engine)``` 
when you will run your app.