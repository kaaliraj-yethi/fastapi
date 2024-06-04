from fastapi import APIRouter
from users import router as users_router
from items import router as items_router

router = APIRouter (prefix="/v1")

router.include_router(users_router)

router.include_router(items_router)


