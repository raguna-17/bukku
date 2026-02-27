from fastapi import APIRouter
from .auth_routes import router as auth_router
from .users import router as user_router
from .tags import router as tag_router
from .bookmarks import router as bookmark_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(user_router, tags=["Users"])
api_router.include_router(tag_router, tags=["Tags"])
api_router.include_router(bookmark_router, tags=["Bookmarks"])