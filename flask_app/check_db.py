import sqlite3

DATABASE = "fastpost.db"

def check_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return tables

if __name__ == "__main__":
    tables = check_db()
    print("Tables in the database:", tables)