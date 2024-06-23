"""middleware file"""
from fastapi import Request
from src.configs.env import get_settings
from src.db.session import db_session
from src.main import app
from src.configs.constants import RESPONSE_HEADERS


config = get_settings()


@app.middleware("http")
async def close_db_connection(request: Request, call_next):
    """close db connection"""
    response = await call_next(request)
    for key, value in RESPONSE_HEADERS.items():
        if config.env != 'local':
            response.headers[key] = value

    db = db_session.get()
    if db:
        db.close()
    return response
