from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as user_models
from ..persistence.model import PaymentModel as payment_models
from ..persistence.schemas import PaymentSchema as schemas
from datetime import datetime

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

@router.post("/", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, user: user_models.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    db_payment = payment_models.Payment(
        userId=user.id,
        paymentId=payment.paymentId,
        value=payment.value,
        status=payment.status,
        date=datetime.utcnow()
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/", response_model=List[schemas.PaymentResponse])
def read_payments(user: user_models.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    stmt = select(payment_models.Payment).where(payment_models.Payment.userId == user.id)
    payments = db.execute(stmt).scalars().all()
    return payments
