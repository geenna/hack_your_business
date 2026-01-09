import sqlite3

# Connect to the database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Add new columns to the users table
try:
    cursor.execute("ALTER TABLE users ADD COLUMN telefono TEXT")
    print("Column 'telefono' added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error adding column 'telefono': {e}")

# Commit changes and close connection
conn.commit()
conn.close()
