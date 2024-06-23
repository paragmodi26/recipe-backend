"""user controller file"""
from contextvars import ContextVar
from datetime import timedelta
from src.configs.constants import SessionConstant
from src.configs.env import get_settings
from src.configs.error_constants import ErrorMessage
from src.services.user.model import UserModel
from src.services.user.serializer import(
    UserInbound, UserLoginInbound, UserAppOutBound, UserFinalOutbound,
    LoginOutbound, LoginFinalOutbound
)
from src.utils.common import encrypt_password, decrypt_password, create_access_token
from src.utils.common_serializers import SuccessResponsePartial
from src.utils.time import get_current_datetime

config = get_settings()
user_details_context: ContextVar[UserAppOutBound] = ContextVar("user_details")


class UserController:
    """controller class for user service"""

    @classmethod
    async def save(cls, payload: UserInbound):
        """user save"""
        user_data = UserModel.get_user_login(email=payload.email, mobile_no=payload.mobile_no)
        if user_data and (user_data.email == payload.email or user_data.mobile_no == payload.mobile_no):
            message = "User Email already exists" if user_data.email == payload.email else "User Mobile Number already exists"
            return SuccessResponsePartial(
                status="error",
                message=ErrorMessage.CUSTOM_MESSAGE.format(message)
            )
        payload.password = encrypt_password(payload.password)
        payload_dict = payload.dict()
        data = UserModel.create(**payload_dict)
        data = UserAppOutBound(
            id=data.id,
            name=data.name,
            email=data.email,
            mobile_no=data.mobile_no
        )
        return UserFinalOutbound(data=data, message="User Registered Successfully, Please Log in")

    @classmethod
    async def user_login(cls, payload: UserLoginInbound):
        """user login"""
        user_data = UserModel.get_user(email=payload.email)
        if not user_data:
            return SuccessResponsePartial(status="error", message=ErrorMessage.CUSTOM_MESSAGE.format("Email Not Found"))
        valid_password = decrypt_password(user_data.password, payload.password)
        if not valid_password:
            return SuccessResponsePartial(status="error", message=ErrorMessage.CUSTOM_MESSAGE.format("Password Mismatch"))
        access_token_expires = timedelta(minutes=SessionConstant.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"email": user_data.email}, expires_delta=access_token_expires
        )
        response = LoginOutbound(access_token=access_token, token_type="bearer")
        return LoginFinalOutbound(data=response, message="User Login Successful")

    @classmethod
    async def user_logout(cls):
        """user logout"""
        user_details = user_details_context.get()
        UserModel.patch(_id=user_details.id, **{"last_login": get_current_datetime()})
        return SuccessResponsePartial(message=ErrorMessage.CUSTOM_MESSAGE.format("User logged out successfully"))
