# scripts/migrate_to_postgres.py

import pandas as pd
from database.db_engine import get_engine, get_postgres_engine

# Engines
mysql_engine = get_engine()
postgres_engine = get_postgres_engine()

def migrate_table(table_name):
    print(f"🔄 Migrating `{table_name}` from MySQL ➜ PostgreSQL")

    # Read from MySQL
    df = pd.read_sql(f"SELECT * FROM {table_name}", mysql_engine)

    if df.empty:
        print(f"⚠️ No data in `{table_name}`")
        return

    print(f"✅ Loaded {len(df)} rows from `{table_name}`")

    # Drop auto ID if exists (Postgres uses SERIAL)
    if "id" in df.columns:
        df = df.drop(columns=["id"])

    # Insert into PostgreSQL
    df.to_sql(table_name, postgres_engine, if_exists="append", index=False, method="multi")
    print(f"✅ Inserted into `{table_name}` on PostgreSQL")

if __name__ == "__main__":
    migrate_table("crypto_prices")
    migrate_table("crypto_metrics")
