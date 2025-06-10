import sqlite3
from crewai.tools import tool

@tool("Get database schema and sample data")
def get_db_schema_with_data(db_path="sample_data/sample.db", sample_limit=5):
    """Returns the schema and sample rows from each table in the SQLite DB."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_with_data = {}
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        cursor.execute(f"SELECT * FROM {table_name} LIMIT {sample_limit};")
        rows = cursor.fetchall()

        schema_with_data[table_name] = {
            "schema": columns,
            "sample_rows": rows
        }

    conn.close()
    return schema_with_data