"""test auth module"""
import random

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.session import get_db
from src.main import config, app
from src.schema.schema import Base

engine = create_engine(
    "postgresql://{user}:{password}@{host}/{db_name}".format(
        user=config.db_app.db_username,
        password=config.db_app.db_password,
        host=config.db_app.db_host,
        db_name=config.db_app.db_name,
    ),
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
number = random.randint(100, 9999)


@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080/rich/api/v1/user") as ac:
        response = await ac.post("/save", json={
            "name": f"testuser{number}",
            "email": f"test{number}@gmail.com",
            "password": "password",
            "mobile_no": f"1234567{number}"
            }
        )
    assert response.status_code == 200
    assert response.json()['status'] == "success"
    assert response.json()['data']['name'] == f"testuser{number}"
    assert response.json()['data']['email'] == f"test{number}@gmail.com"
    assert response.json()['data']['mobile_no'] == f"1234567{number}"


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080/rich/api/v1/user") as ac:
        response = await ac.post("/login", json={"email": f"test{number}@gmail.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()['status'] == "success"
    assert response.json()['data']['token_type'] == "bearer"
