"""Route for ping"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("")
def ping():
    """Ping"""
    return JSONResponse(content={"service": "ok"}, status_code=200)
