from sqlalchemy import create_engine
from config.settings import DB_URL,DB_POSTGRES_URL,DEPLOYMENT

def get_engine():
    """
    Creates and returns a SQLAlchemy engine using the Local database URL.

    Returns:
        sqlalchemy.Engine: SQLAlchemy engine connected to the specified DB.
    """
    engine = create_engine(DB_URL, echo=False, future=True)
    return engine

def get_postgres_engine():
    """
    Cloud PostgreSQL engine — used only for deployment or migration.
    """
    return create_engine(DB_POSTGRES_URL, echo=False, future=True)

def _choose_engine(engine_type: str = "auto"):
    """
    Chooses the appropriate database engine based on deployment status.
    """
    if engine_type == "cloud" or DEPLOYMENT == "1":
        return get_postgres_engine()
    return get_engine()