"""user auth functions"""
import jwt
from fastapi import Request
from functools import wraps
from src.configs.constants import SessionConstant
from src.configs.env import get_settings
from src.configs.error_constants import ErrorMessage
from src.services.user.controller import user_details_context
from src.services.user.model import UserModel
from src.services.user.serializer import UserAppOutBound
from src.utils.common_serializers import SuccessResponsePartial

config = get_settings()
revoked_tokens = set()


class Auth:
    """auth class"""

    @classmethod
    def authenticate_user(cls, func):
        """Authentication request"""
        @wraps(func)
        async def check_user(request: Request, *args, **kwargs):
            """Authentication request"""
            token = request.headers.get('authorization')
            token = token.split(" ")[-1]
            if not token:
                return SuccessResponsePartial(status="error", message=ErrorMessage.AUTH_TOKEN_MISSING)
            try:
                session = jwt.decode(token, SessionConstant.SECRET_KEY, algorithms=[SessionConstant.ALGORITHM])
            except jwt.ExpiredSignatureError:
                return SuccessResponsePartial(status="error", message="Token is expired please login again")
            except Exception as ex:
                return SuccessResponsePartial(status="error", message="Token is expired please login again")
            email = session.get("email") if session and isinstance(session, dict) else None
            if not session or not email or token in revoked_tokens:
                return SuccessResponsePartial(status="error", message=ErrorMessage.INVALID_TOKEN)
            user_data = UserModel.get_user(email=email)
            if not user_data:
                return SuccessResponsePartial(status="error", message=ErrorMessage.INVALID_USER)
            user_data = UserAppOutBound(**user_data.__dict__)
            user_details_context.set(user_data)
            return await func(request, *args, **kwargs)
        return check_user

    @classmethod
    def logout_user(cls, func):
        """Authentication request"""
        @wraps(func)
        async def revoked_token(request: Request, *args, **kwargs):
            """revoked token"""
            token = request.headers.get('authorization')
            token = token.split(" ")[-1]
            if not token:
                return SuccessResponsePartial(status="error", message=ErrorMessage.AUTH_TOKEN_MISSING)
            revoked_tokens.add(token)
            return await func(request, *args, **kwargs)
        return revoked_token
