from sqlalchemy import Column, String, ForeignKey, Float, DateTime
import uuid
from datetime import datetime
from ..database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(String, ForeignKey("users.id", ondelete="RESTRICT"))
    paymentId = Column(String)
    value = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    tipoPagamento = Column(String)
