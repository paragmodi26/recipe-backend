"""schema file"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UniqueConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    JSONB,
    SMALLINT,
    TIMESTAMP,
    VARCHAR,
    TEXT
)
from sqlalchemy.orm import relationship
from src.configs.db_constants import DBConfig, DBTables


Base = declarative_base()


class UsersSchema(Base):
    """users model class"""
    __tablename__ = DBTables.USERS
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True, index=True)
    name                = Column(VARCHAR(200), nullable=False)
    email               = Column(VARCHAR(100), nullable=False, unique=True)
    mobile_no           = Column(VARCHAR(250), nullable=False)
    password            = Column(VARCHAR(255), nullable=False)
    created_on          = Column(TIMESTAMP, nullable=True)
    updated_on          = Column(TIMESTAMP, nullable=True)
    last_login          = Column(TIMESTAMP, nullable=True)
    status              = Column(SMALLINT, nullable=False, default=1)
    recipes             = relationship("RecipeSchema", back_populates="user")
    UniqueConstraint(email, name="user_auth_email_key")


class RecipeSchema(Base):
    """recipie model class"""
    __tablename__ = DBTables.RECIPE
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True, index=True)
    name                = Column(VARCHAR(250), nullable=False)
    title               = Column(VARCHAR(255), nullable=False)
    description         = Column(TEXT, nullable=True)
    ingredients         = Column(JSONB, default=lambda: {})
    instructions        = Column(TEXT, nullable=True)
    created_by          = Column(BIGINT, ForeignKey(UsersSchema.id, ondelete='CASCADE'))
    user = relationship('UsersSchema', back_populates="recipes")


Index(DBTables.RECIPE + "_name", RecipeSchema.name, unique=False)
Index(DBTables.RECIPE + "_title", RecipeSchema.title, unique=False)
Index(DBTables.USERS + "_email", UsersSchema.email, unique=False)
Index(DBTables.USERS + "_mobile_no", UsersSchema.mobile_no, unique=False)
