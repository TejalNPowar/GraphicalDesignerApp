import sqlite3

DB_NAME = "graphic_designer_management.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Stock table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        material TEXT,
        quantity REAL,
        cost REAL
    )
    """)

    # Customer billing table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        work TEXT,
        material TEXT,
        quantity REAL,
        price REAL,
        total REAL,
        paid REAL,
        remaining REAL
    )
    """)

    conn.commit()
    conn.close()
