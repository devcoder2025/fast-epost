import sqlite3
import os
import logging

DATABASE = "fastpost.db"

def check_db():  # Function to check the database and retrieve table names
    if not os.path.exists(DATABASE):
        logging.error(f"Database file '{DATABASE}' does not exist.")
        return []

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()
    return tables

if __name__ == "__main__":
    tables = check_db()
    print("Tables in the database:", tables)
