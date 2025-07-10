from sqlalchemy import text
import pandas as pd
from database.db_engine import get_engine

def create_table_from_sql():
    """
    Creates the 'crypto_prices' table in the database using the schema defined in models.sql.
    """
    engine = get_engine()
    with engine.begin() as conn:
        with open("database/models.sql") as f:
            sql_script = f.read()
            
        # Split by semicolon and run each create statement separately
        statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]
        for stmt in statements:
            conn.execute(text(stmt))

            
def insert_crypto_prices(df: pd.DataFrame):
    """
    Inserts the given DataFrame of crypto prices into the database table 'crypto_prices'.

    Args:
        df (pd.DataFrame): DataFrame with columns matching the database schema.
    """
    engine = get_engine()
    
    
    with engine.begin() as conn:
        df.to_sql("crypto_prices", con=conn, if_exists="append", index=False)
        
def insert_crypto_metrics(df: pd.DataFrame):
    """
    Inserts computed metrics into the 'crypto_metrics' table

    Args:
        df (pd.DataFrame): DataFrame with columns:
        ['coin_id', 'symbol', 'rolling_mean_7d', 'volatility_24h',"cv_24h", 'computed_at', 'granularity']
    """
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql('crypto_metrics', con=conn, if_exists="append", index=False)