from ..persistence.model import PaymentModel as payment_models
from sqlalchemy.orm import Session

def aggiungiPagamento(db: Session, paymentModel: payment_models.Payment):
    db.add(paymentModel)
    db.commit()
    db.refresh(paymentModel)
    return paymentModel