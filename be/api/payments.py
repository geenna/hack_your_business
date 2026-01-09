from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as user_models
from ..persistence.model import PaymentModel as payment_models
from ..persistence.schemas import PaymentSchema as schemas
from ..persistence.schemas import BillingAddressSchema 
from ..service import billing_service
from ..persistence.model.BillingAddressModel import BillingAddressModel
from datetime import datetime

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)
allow_admin_only = auth.RoleChecker(["all"])
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

    payments = db.execute(stmt).scalars().all()
    return payments

@router.put("/address-data", response_model=BillingAddressSchema.BillingAddressSchema)
def update_billing_address(
    address_data: BillingAddressSchema.BillingAddressSchema,
    user: user_models.User = Depends(allow_admin_only), 
    db: Session = Depends(auth.get_db)
):
    # Convert Pydantic model to SQLAlchemy model
    # We create a new instance or update existing logic is handled in service, 
    # but the service expects a model object to copy fields from.
    # Note: address_data might have empty id/userId which we should override/ignore
    
    billing_address_model = BillingAddressModel(
        userId=user.id,
        regSociale=address_data.regSociale,
        piva=address_data.piva,
        address=address_data.address,
        city=address_data.city,
        cap=address_data.cap,
        stato=address_data.stato,
        prov=address_data.prov
    )
    
    updated_address = billing_service.add_or_edit_billing_address(
        user_id=user.id,
        new_address=billing_address_model,
        db=db
    )
    
    return updated_address
