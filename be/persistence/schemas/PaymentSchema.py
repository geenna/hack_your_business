from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    paymentId: str
    value: float
    status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: str
    userId: str
    date: datetime

    class Config:
        from_attributes = True
