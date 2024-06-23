"""main file"""
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.configs.constants import APP_CONTEXT_PATH, APP_CONTEXT_PATH_INTERNAL
from src.versions.v1 import main as v1_route
from src.versions.v1 import internal as v1_internal_route
from fastapi.middleware.gzip import GZipMiddleware
from src.configs.env import get_settings


config = get_settings()


app = FastAPI(
    title="Rich Master APIs",
    description="Rich Master APIs"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(v1_route.api_router, prefix=APP_CONTEXT_PATH)
app.include_router(v1_internal_route.api_router, prefix=APP_CONTEXT_PATH_INTERNAL)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
