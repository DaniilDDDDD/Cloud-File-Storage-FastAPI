import uvicorn
from fastapi import FastAPI

from core.database import database
from core.routes import router

from admin.admin_setup import admin_start

app = FastAPI()
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(router, prefix='/api')

if __name__ == '__main__':
    # admin_start()
    uvicorn.run(app)
