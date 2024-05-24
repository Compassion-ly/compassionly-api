from fastapi import APIRouter

from app.api.routes import auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"], prefix="/auth")
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

