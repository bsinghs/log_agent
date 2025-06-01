import sqlite3

def get_user_by_email(email):
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    try:
        # Intentionally using a wrong column name 'emails' instead of 'email'
        cursor.execute("SELECT * FROM users WHERE emails = ?", (email,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print("Database error:", e)
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    print(get_user_by_email("test@example.com"))
