import os
import sqlite3

def init_db(db_name="data.db"):
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # CRITICAL: Enable Foreign Key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Product Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    # 2. Create Stock Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            p_id INTEGER PRIMARY KEY,
            qty INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (p_id) REFERENCES product (id) ON DELETE CASCADE
        )
    ''')

    # 3. Create Sale Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL
        )
    ''')

    # 4. Create Sale_Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            s_id INTEGER,
            p_name TEXT NOT NULL,
            p_price INTEGER NOT NULL,
            FOREIGN KEY (s_id) REFERENCES sale (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized successfully.")

if __name__ == "__main__":
    if os.path.exists("data.db"):
        print("Database already exists.")
    else:
        init_db()