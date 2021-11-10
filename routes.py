from fastapi import APIRouter

from api.views import router as files_router
from users.routers import users_router

router = APIRouter()

router.include_router(files_router, tags=['Files'])
router.include_router(users_router, tags=['Users'])
