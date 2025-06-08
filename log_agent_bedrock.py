import os
import json
import sqlite3
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")  # or your chosen region
CLAUDE_MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"


def read_log_file(file_path):
    """Reads the log file and returns its content."""
    with open(file_path, "r") as f:
        return f.read()


def get_db_schema_with_data(db_path="sample.db", sample_limit=5):
    """Returns schema and sample rows from each table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_with_data = {}
    for (table_name,) in tables:
        # Schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info = [
            {
                "name": col[1],
                "type": col[2],
                "notnull": bool(col[3]),
                "default": col[4],
                "primary_key": bool(col[5]),
            }
            for col in columns
        ]

        # Sample Data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {sample_limit};")
        rows = cursor.fetchall()

        schema_with_data[table_name] = {"schema": schema_info, "sample_rows": rows}

    conn.close()
    return schema_with_data


def analyze_log_and_system(log_text, schema, code_snippets):
    prompt = f"""
Human: I have this database schema and some sample data:

{json.dumps(schema, indent=2)}

And this error log:

{log_text}

And the following code snippets:

{code_snippets}

Please figure out whether the issue is in the database or the code, and suggest a fix. If it's a code issue, give a corrected code snippet. If it's a database issue, give the SQL query or data correction needed.

Assistant:
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": "Explain the error: no such column: emails in my SQL query"
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=CLAUDE_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]  # Claude v3 responses



def read_code_files(directory="code_snippet", extensions=(".py",), max_files=5):
    """Reads up to `max_files` Python files in the given directory."""
    import os

    code_snippets = []
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    code_snippets.append((file, content))
                    count += 1
                if count >= max_files:
                    break
        if count >= max_files:
            break

    return code_snippets

def maybe_execute_sql_fix(suggestion, db_path="sample.db"):
    import sqlite3
    import re

    # Try to extract SQL queries from the suggestion
    sql_candidates = re.findall(r"(SELECT|UPDATE|DELETE|INSERT|ALTER|CREATE|DROP).*?;", suggestion, re.IGNORECASE | re.DOTALL)
    
    if not sql_candidates:
        print("ℹ️ No valid SQL query detected. Looks like the fix is in the code, not the database.")
        return

    print("\n⚠️ Detected SQL Query:\n")
    for query in sql_candidates:
        print(query.strip())

    confirm = input("\nDo you want to run this query on the database? (yes/no): ").lower()
    if confirm != "yes":
        print("🛑 Skipped execution.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for query in sql_candidates:
            cursor.execute(query.strip())
        conn.commit()
        print("✅ SQL query executed successfully.")
    except Exception as e:
        print("❌ Error executing query:", e)
    finally:
        conn.close()

def save_to_memory(log_text, suggestion, memory_path="agent_memory.json"):
    memory = []
    if os.path.exists(memory_path):
        with open(memory_path, "r") as f:
            memory = json.load(f)

    memory.append({"log": log_text, "suggestion": suggestion})

    with open(memory_path, "w") as f:
        json.dump(memory, f, indent=2)

if __name__ == "__main__":
    log_content = read_log_file("error.log")
    schema_with_data = get_db_schema_with_data()
    code_snippets = read_code_files(directory="code_snippet", extensions=(".py",))

    result = analyze_log_and_system(log_content, schema_with_data, code_snippets)

    print("=== Suggestions from GPT ===")
    print(result)

    maybe_execute_sql_fix(result)
