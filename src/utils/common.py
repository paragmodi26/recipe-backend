"""common functions"""
import bcrypt
import jwt
from datetime import timedelta
from typing import Union
from src.configs.constants import SessionConstant
from src.utils.time import get_current_datetime


def encrypt_password(password):
    """Encrypt password"""
    pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    password_hash = pwhash.decode('utf8')
    return password_hash


def decrypt_password(hashed_password, input_password):
    """Decrypt password"""
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """function to generate access token"""
    to_encode = data.copy()
    expires_delta = expires_delta or timedelta(minutes=SessionConstant.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = get_current_datetime(return_string=False) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SessionConstant.SECRET_KEY, algorithm=SessionConstant.ALGORITHM)
    return encoded_jwt
