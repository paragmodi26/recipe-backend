"""Tests for schemas module."""
import random
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import config
from src.schema.schema import Base, UsersSchema, RecipeSchema
from src.utils.common import encrypt_password

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
number = random.randint(100, 999)
number_1 = random.randint(100, 999)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_create_user(db_session):
    password = encrypt_password("password")
    user = UsersSchema(**
                       {
                            "name": f'testuser{number}',
                            "mobile_no": f"5656565{number}",
                            "email": f"test{number}@gmail.com",
                            "password": password
                        }
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert db_session.query(UsersSchema).filter(UsersSchema.email==f"test{number}@gmail.com").count() == 1


def test_create_recipe(db_session):
    password = encrypt_password("password")
    user = UsersSchema(**
                       {
                            "name": f'testuser{number}',
                           "mobile_no": f"5656565{number}",
                           "email": f"test{number}@gmail.com",
                           "password": password
                       }
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    recipe = RecipeSchema(**{
        "name": "test recipe",
        "title": "Test Recipe",
        "description": "This is a test recipe",
        "ingredients": [{"name": "Test Ingredients", "quantity": "1"}],
        "instructions": "Test Instructions",
        "created_by": user.id,
    })
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    assert db_session.query(RecipeSchema).filter(RecipeSchema.name == "test recipe").count() == 1
