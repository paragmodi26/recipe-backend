"""user route file"""
from fastapi import APIRouter, Request
from src.services.user.controller import UserController
from src.services.user.serializer import UserInbound, UserLoginInbound
from src.utils.auth import Auth


router = APIRouter()


@router.post("/save")
async def save(request: Request, payload: UserInbound):
    """user save"""
    return await UserController.save(payload=payload)


@router.post("/login")
async def login(request: Request, payload: UserLoginInbound):
    """user login"""
    return await UserController.user_login(payload=payload)


@router.get("/logout")
@Auth.authenticate_user
@Auth.logout_user
async def logout(request: Request):
    """user logout"""
    return await UserController.user_logout()
