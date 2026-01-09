from pydantic import BaseModel
from typing import Optional

class BillingAddressSchema(BaseModel):
    id: str
    userId: str
    regSociale: Optional[str] = None
    piva: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    cap: Optional[str] = None
    stato: Optional[str] = None
    prov: Optional[str] = None

    class Config:
        from_attributes = True
