"""global constant file"""
from src.configs.env import get_settings


config = get_settings()
APP_CONTEXT_PATH = "/rich/api"
APP_CONTEXT_PATH_INTERNAL = "/rich-internal/api"

RESPONSE_HEADERS = {
    "X-XSS-Protection": "1; mode=block",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Option": "deny",
    "Strict-Transport-Security": "deny",
    "Content-Security-Policy": "script-src 'self'",
}


class Constants:
    """global constants"""
    DEFAULT_TIME_ZONE = "UTC"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"


class ValidationConstant:
    """Constants related to data validations"""

    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    PHONE_REGEX = r"^[ ()\+\-\d]*$"


class SessionConstant:
    """session constant"""
    SECRET_KEY = config.jwt_secret_key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 120
