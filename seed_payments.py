import sqlite3
import uuid
import random
from datetime import datetime, timedelta

DB_PATH = "sql_app.db"

def migrate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(payments)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if "tipoPagamento" not in columns:
        print("Adding tipoPagamento column...")
        cursor.execute("ALTER TABLE payments ADD COLUMN tipoPagamento VARCHAR")
        conn.commit()
    else:
        print("Column tipoPagamento already exists.")
    conn.close()

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    user_id = "9f48fe31-6ffd-4ece-9361-b9831cd9a6ef"
    statuses = ["PAGATO", "IN ATTESA", "RIFIUTATO", "ANNULLATO"]
    types = ["STRIPE", "BONIFICO", "CONTANTI"]
    
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2026, 1, 10)
    delta_days = (end_date - start_date).days
    
    print(f"Seeding 30 records for user {user_id}...")
    
    for _ in range(30):
        payment_id = f"PAY-{random.randint(10000, 99999)}"
        value = random.uniform(500, 1000)
        random_days = random.randint(0, delta_days)
        date_val = start_date + timedelta(days=random_days)
        status = random.choice(statuses)
        tipo = random.choice(types)
        rec_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO payments (id, userId, paymentId, value, date, status, tipoPagamento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (rec_id, user_id, payment_id, value, date_val, status, tipo))
        
    conn.commit()
    print("Seeding complete.")
    conn.close()

if __name__ == "__main__":
    migrate_db()
    seed_data()
