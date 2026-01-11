import sqlite3

# Connect to the database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Add new columns to the projects table
try:
    cursor.execute("ALTER TABLE projects ADD COLUMN projectName VARCHAR")
    print("Column 'projectName' added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error adding column 'projectName': {e}")

# Commit changes and close connection
conn.commit()
conn.close()
