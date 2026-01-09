from sqlalchemy import Column, String, ForeignKey
import uuid
from ..database import Base

class BillingAddressModel(Base):
    __tablename__ = "billing_address"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(String, ForeignKey("users.id"))
    regSociale = Column(String)
    piva = Column(String)
    address = Column(String)
    city = Column(String)
    cap = Column(String)
    stato = Column(String)
    prov = Column(String)
