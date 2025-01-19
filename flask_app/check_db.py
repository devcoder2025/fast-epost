import sqlite3

DATABASE = "fastpost.db"

def check_db():  # Function to check the database and retrieve table names
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()
    return tables

if __name__ == "__main__":
    tables = check_db()
    print("Tables in the database:", tables)
