"""main route file"""
from fastapi import APIRouter
from src.versions.v1.routes import user, recipe

api_router = APIRouter()
api_router.include_router(user.router, prefix="/v1/user", tags=["User"])
api_router.include_router(recipe.router, prefix="/v1/recipe", tags=["Recipe"])
