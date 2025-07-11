# # this was done only for local data base before-----------

# from sqlalchemy import text
# import pandas as pd
# from database.db_engine import get_engine

# def create_table_from_sql(schema_file="database/models.sql"):
#     """
#     Reads SQL statements from a given schema file and executes them.
#     Supports both MySQL and PostgreSQL versions.
#     """
#     from database.db_engine import get_engine
#     from sqlalchemy import text

#     with open(schema_file, "r") as file:
#         raw_sql = file.read()

#     statements = [stmt.strip() for stmt in raw_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]

#     engine = get_engine()
#     with engine.begin() as conn:
#         for stmt in statements:
#             conn.execute(text(stmt + ";"))

#     print(f"✅ Tables created using {schema_file}")

            
# def insert_crypto_prices(df: pd.DataFrame):
#     """
#     Inserts the given DataFrame of crypto prices into the database table 'crypto_prices'.

#     Args:
#         df (pd.DataFrame): DataFrame with columns matching the database schema.
#     """
#     engine = get_engine()
    
    
#     with engine.begin() as conn:
#         df.to_sql("crypto_prices", con=conn, if_exists="append", index=False)
        
# def insert_crypto_metrics(df: pd.DataFrame):
#     """
#     Inserts computed metrics into the 'crypto_metrics' table

#     Args:
#         df (pd.DataFrame): DataFrame with columns:
#         ['coin_id', 'symbol', 'rolling_mean_7d', 'volatility_24h',"cv_24h", 'computed_at', 'granularity']
#     """
#     engine = get_engine()
#     with engine.begin() as conn:
#         df.to_sql('crypto_metrics', con=conn, if_exists="append", index=False)

# # -------------------this is for both mysql and postgres --------------

from sqlalchemy import text
import pandas as pd
from database.db_engine import get_engine, get_postgres_engine


def _choose_engine(engine_type: str = "local"):
    if engine_type == "cloud":
        return get_postgres_engine()
    return get_engine()


def create_table_from_sql(schema_file="database/models.sql", engine_type="local"):
    """
    Reads SQL statements from schema file and executes them on the specified DB engine.

    Args:
        schema_file (str): Path to the SQL schema.
        engine_type (str): 'local' for MySQL or 'cloud' for PostgreSQL.
    """
    engine = _choose_engine(engine_type)

    with open(schema_file, "r") as file:
        raw_sql = file.read()

    # Skip empty or comment-only lines
    statements = [stmt.strip() for stmt in raw_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]

    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt + ";"))

    print(f"✅ Tables created using {schema_file} on {engine_type} DB")


def insert_crypto_prices(df: pd.DataFrame, engine_type="local"):
    """
    Inserts a DataFrame of crypto prices into the 'crypto_prices' table.

    Args:
        df (pd.DataFrame): Cleaned data.
        engine_type (str): 'local' or 'cloud'
    """
    engine = _choose_engine(engine_type)
    with engine.begin() as conn:
        df.to_sql("crypto_prices", con=conn, if_exists="append", index=False)


def insert_crypto_metrics(df: pd.DataFrame, engine_type="local"):
    """
    Inserts computed metrics into the 'crypto_metrics' table.

    Args:
        df (pd.DataFrame): DataFrame with metrics.
        engine_type (str): 'local' or 'cloud'
    """
    engine = _choose_engine(engine_type)
    with engine.begin() as conn:
        df.to_sql("crypto_metrics", con=conn, if_exists="append", index=False)
