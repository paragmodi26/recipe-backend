"""user serializer"""
from typing import Optional
from pydantic import BaseModel, constr, validator
from src.configs.constants import ValidationConstant
from src.utils.common_serializers import SuccessResponsePartial


class UserLoginInbound(BaseModel):
    """User Login Inbound Model"""
    email: constr(strict=True, max_length=50, strip_whitespace=True, pattern=ValidationConstant.EMAIL_REGEX)
    password: constr(strict=True, max_length=50, strip_whitespace=True, min_length=8)

    @validator("email", pre=True)
    def validate_email(cls, value):
        if value:
            return value.lower()


class UserInbound(UserLoginInbound):
    """User Inbound Model"""
    name: constr(strict=True, strip_whitespace=True, max_length=100)
    mobile_no: constr(strict=True, strip_whitespace=True, max_length=50, pattern=ValidationConstant.PHONE_REGEX)


class UserAppOutBound(BaseModel):
    """User App Inbound Model"""
    id: Optional[int] = None
    name: str
    email: str
    mobile_no: str

    class Config:
        """Config"""
        from_attributes = True


class UserFinalOutbound(SuccessResponsePartial):
    """User Final Outbound Model"""
    data: UserAppOutBound = None


class LoginOutbound(BaseModel):
    """login outbound"""
    access_token: str
    token_type: str


class LoginFinalOutbound(SuccessResponsePartial):
    """login final outbound"""
    data: LoginOutbound = None
