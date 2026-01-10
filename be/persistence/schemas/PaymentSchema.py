from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    paymentId: str
    value: float
    status: str
    tipoPagamento: Optional[str] = None

class PaymentCreate(BaseModel):
    value: float
    status: str
    tipoPagamento: Optional[str] = None
    userId: str
    date: datetime

class PaymentResponse(PaymentBase):
    id: str
    userId: str
    date: datetime

    class Config:
        from_attributes = True
