from sqlalchemy.orm import Session
from sqlalchemy import select
from ..persistence.model import UserModel, PaymentModel

def get_users_with_payments(db: Session):
    # Query all users
    stmt_users = select(UserModel.User)
    users = db.execute(stmt_users).scalars().all()
    
    result = []
    for user in users:
        # For each user, get payments
        # Note: Ideally we should use a JOIN or relationship, but this is a "simple" service implementation as requested
        stmt_payments = select(PaymentModel.Payment).where(PaymentModel.Payment.userId == user.id)
        payments = db.execute(stmt_payments).scalars().all()
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "nome": user.nome,
            "cognome": user.cognome,
            "payments": [
                {
                    "paymentId": p.paymentId,
                    "value": p.value,
                    "status": p.status,
                    "date": p.date.isoformat() if p.date else None
                } for p in payments
            ]
        }
        result.append(user_data)
        
    return result

def get_users_with_payments_v2(db: Session):
    # Optimized query using JOIN
    # Performs a Left Outer Join to get all users and their payments (if any) in a single query
    stmt = select(UserModel.User, PaymentModel.Payment).join(
        PaymentModel.Payment, 
        UserModel.User.id == PaymentModel.Payment.userId, 
        isouter=True
    )
    rows = db.execute(stmt).all()

    # Aggregate results in Python
    # Dictionary to hold user_id -> user_data mapping
    users_map = {}

    for user, payment in rows:
        if user.id not in users_map:
            users_map[user.id] = {
                "id": user.id,
                "email": user.email,
                "nome": user.nome,
                "cognome": user.cognome,
                "payments": []
            }
        
        if payment:
            users_map[user.id]["payments"].append({
                "paymentId": payment.paymentId,
                "value": payment.value,
                "status": payment.status,
                "date": payment.date.isoformat() if payment.date else None
            })

    return list(users_map.values())
