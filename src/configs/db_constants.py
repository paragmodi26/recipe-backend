
class DBTables:
    """db tables"""

    USERS                 = "users"
    RECIPE                = "recipe"


class DBConfig:
    """db configs"""
    SCHEMA_NAME = "recipe_db"
    BASE_ARGS = {"schema": SCHEMA_NAME}
