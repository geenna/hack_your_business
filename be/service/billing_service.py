from ..persistence.model.BillingAddressModel import BillingAddressModel 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def add_or_edit_billing_address(user_id: str, 
                                new_address: BillingAddressModel, 
                                db: Session):
    
    # Use correct class BillingAddress and field userId
    db_address = db.query(BillingAddressModel).filter(BillingAddressModel.userId == user_id).first()

    if db_address:
        # UPDATE: Update existing fields from the passed SQLAlchemy object
        # new_address is a SQLAlchemy object, so we access attributes directly
        db_address.regSociale = new_address.regSociale
        db_address.piva = new_address.piva
        db_address.address = new_address.address
        db_address.city = new_address.city
        db_address.cap = new_address.cap
        db_address.stato = new_address.stato
        db_address.prov = new_address.prov
    else:
        # INSERT: Create new address
        db_address = new_address
        # Ensure userId is set (though it should be passed in construction)
        db_address.userId = user_id
        db.add(db_address)
    
    try:
        db.commit()
        db.refresh(db_address)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Database integrity error. Check provided data."
        )

    return db_address
    