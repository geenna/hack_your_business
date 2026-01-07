
from be.persistence.database import SessionLocal
from be.persistence.model import UserModel as models
import json

def update_users():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print(f"Found {len(users)} users.")
        for user in users:
            print(f"Checking user {user.email}...")
            # We enforce the update again
            new_roles = [{"action": "all", "subject": "manage"}]
            user.roles = new_roles
            print(f"  -> Set roles to: {new_roles}")
        
        db.commit()
        print("All users updated successfully.")
        
        # Verify
        print("\nVerification:")
        for user in db.query(models.User).all():
            print(f"  {user.email}: {user.roles}")

    except Exception as e:
        print(f"Error updating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_users()
