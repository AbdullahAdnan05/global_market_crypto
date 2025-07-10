from sqlalchemy import create_engine
from config.settings import DB_URL

def get_engine():
    """
    Creates and returns a SQLAlchemy engine using the database URL.

    Returns:
        sqlalchemy.Engine: SQLAlchemy engine connected to the specified DB.
    """
    engine = create_engine(DB_URL, echo=False, future=True)
    return engine