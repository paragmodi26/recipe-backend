"""recipie Unit tests for recipie.py"""
import random
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.session import Base, get_db
from src.main import config, app
glo_token = set()


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
async def create_user():
    """Fixture to create a test user"""
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080/rich/api/v1/user") as ac:
        response = await ac.post("/save", json={
            "name": f"test{number}",
            "mobile_no": f"12345678{number}",
            "email": f"test{number}@gmail.com",
            "password": "password"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"]["name"] == f"test{number}"


@pytest.mark.asyncio
async def login():
    """Helper function to register a user and get an authentication token"""
    await create_user()
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080/rich/api/v1/user") as ac:
        login_response = await ac.post("/login", json={
            "email": f"test{number}@gmail.com",
            "password": "password"
        })
        assert login_response.status_code == 200
        token = login_response.json()["data"]["access_token"]
        assert token is not None
        glo_token.add(token)
        return token


@pytest.mark.asyncio
async def test_create_recipe():
    """Test case to create a new recipe"""
    await login()
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080/rich/api/v1/recipe") as ac:
        response = await ac.post("/save", json={
            "title": "Test Recipe",
            "name": "Test Recipe",
            "description": "A test recipe",
            "ingredients": [
                {
                    "name": "Test ingredients",
                    "quantity": "1"
                }
            ],
            "instructions": "Test instructions"
        }, headers={"Authorization": f"Bearer {list(glo_token)[0]}"})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Recipe saved successfully"


@pytest.mark.asyncio
async def test_get_recipes():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080/rich/api/v1/recipe") as ac:
        response = await ac.get("/all", headers={"Authorization": f"Bearer {list(glo_token)[0] }"})
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
