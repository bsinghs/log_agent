import sqlite3


def create_sample_db():
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    # Sample table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """)

    # Insert sample data
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)",
        ("alice", "alice@example.com"),
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)",
        ("bob", "bob@example.com"),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_sample_db()
    print("Sample database created: sample.db")
