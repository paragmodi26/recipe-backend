from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from src.configs.db_constants import DBConfig
from src.schema.schema import Base

from src.configs.env import get_settings
app_config = get_settings()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USERNAME", app_config.db_app.db_username)
config.set_section_option(section, "DB_PASSWORD", app_config.db_app.db_password)
config.set_section_option(section, "DB_NAME", app_config.db_app.db_name)
config.set_section_option(section, "DB_HOST", app_config.db_app.db_host)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    """DB string"""
    return "postgresql://%s:%s@%s/%s" % (
        app_config.db_app.db_username,
        app_config.db_app.db_password,
        app_config.db_app.db_host,
        app_config.db_app.db_name,
    )


def include_object(object, name, type_, reflected, compare_to):
    """include object method"""
    if type_ == "table" and object.schema != DBConfig.SCHEMA_NAME:
        return False
    else:
        return True


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # connection.execute(f"CREATE SCHEMA IF NOT EXISTS {DBConfig.SCHEMA_NAME}")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=DBConfig.SCHEMA_NAME,
            include_object=include_object,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
