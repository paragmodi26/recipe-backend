"""route file for internal route"""
from fastapi import APIRouter
from src.versions.v1.routes import ping


api_router = APIRouter()
api_router.include_router(ping.router, prefix="/v1/ping", tags=["Ping"])


