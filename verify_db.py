from be.persistence.database import SessionLocal, engine, Base
from be.persistence.model.UserModel import User
from be.persistence.model.PaymentModel import Payment
from be.persistence.schemas import UserSchema as schemas
from be.auth import get_password_hash
import uuid

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if user already exists
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        # Create a sample user
        user = User(
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            userType="admin",
            roles=["admin", "user"],
            nome="Mario",
            cognome="Rossi"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created User: ID={user.id}, Email={user.email}, Roles={user.roles}")
    else:
        print(f"User already exists: ID={user.id}, Email={user.email}, Roles={user.roles}")
        user.hashed_password = get_password_hash("password")
        db.commit()
        print("Updated password for existing user")

    # Check/Create Payment
    payment = db.query(Payment).filter(Payment.userId == user.id).first()
    if not payment:
        payment = Payment(
            userId=user.id,
            paymentId="PAY-12345",
            value=100.50,
            status="completed"
        )
        db.add(payment)
        db.commit()
        print("Created sample payment")
    else:
        print("Sample payment already exists")

    # Verify Pydantic schema
    print(f"Pydantic Verification: {user_schema.json()}")

    # Verify Service V2
    from be.service import service_prova
    print("Verifying Service V2 (Joined Query)...")
    v2_result = service_prova.get_users_with_payments_v2(db)
    print(f"V2 Result count: {len(v2_result)}")
    if v2_result:
         print(f"First user payments: {len(v2_result[0]['payments'])}")

finally:
    db.close()
