from app.utils import log
import csv
import os
import sqlite3
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv
from silero_vad import load_silero_vad
from faster_whisper import download_model

def init_db(db_name="data/data.db"):
    if os.path.exists(db_name):
        log(f"Database '{db_name}' already exists. Skipping initialization.")
        return
    
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
            p_qty INTEGER NOT NULL,
            FOREIGN KEY (s_id) REFERENCES sale (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    log(f"Database '{db_name}' initialized successfully.")

def load_csv_data(db_name="data/data.db", root_folder="data/sample-data"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    table_mappings = {
        f"{root_folder}/product.csv": "INSERT INTO product (name, price) VALUES (?, ?)",
        f"{root_folder}/stock.csv": "INSERT INTO stock (p_id, qty) VALUES (?, ?)",
        f"{root_folder}/sale.csv": "INSERT INTO sale (date) VALUES (?)",
        f"{root_folder}/sale_items.csv": "INSERT INTO sale_items (s_id, p_name, p_price, p_qty) VALUES (?, ?, ?, ?)"
    }

    try:
        for filename, query in table_mappings.items():
            
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                
                for row in reader:
                    cursor.execute(query, row)
                    
        conn.commit()
        log("All sample data added to the database")

    except FileNotFoundError as e:
        print(f"❌ Error: Could not find the file - {e.filename}")
        conn.rollback()
    except sqlite3.IntegrityError as e:
        print(f"❌ Foreign Key / Integrity error: {e}")
        conn.rollback()
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

def download_llama_model(repo_id: str, filename: str):
    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
    )
    log(f"Llama model downloaded/setup successfully")

def download_silero_model():
    load_silero_vad()
    log("Silero VAD model downloaded/setup successfully")

def downlad_whisper_model(model_size="medium"):
    download_model(model_size)
    log(f"Whisper model '{model_size}' downloaded/setup successfully")

if __name__ == "__main__":
    load_dotenv()

    init_db()
    load_csv_data()
    download_silero_model()
    downlad_whisper_model()
    download_llama_model(os.getenv("LLAMA_REPO_ID"), os.getenv("LLAMA_FILE_NAME"))
