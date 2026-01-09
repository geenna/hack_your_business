from sqlalchemy import create_engine, text
from be.persistence.database import SQLALCHEMY_DATABASE_URL

def add_user_status_column():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        try:
            # Add user_status column
            connection.execute(text("ALTER TABLE users ADD COLUMN user_status VARCHAR"))
            # Set default value 'ATTIVO' for existing records
            connection.execute(text("UPDATE users SET user_status = 'ATTIVO' WHERE user_status IS NULL"))
            connection.commit()
            print("Migration successful: Added user_status column and backfilled data.")
        except Exception as e:
            print(f"Migration failed or column might already exist: {e}")

if __name__ == "__main__":
    add_user_status_column()
