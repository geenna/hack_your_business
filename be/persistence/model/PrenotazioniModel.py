from sqlalchemy import Column, String, ForeignKey, Date, Boolean
import uuid
from ..database import Base


class Prenotazioni(Base):
    __tablename__ = "prenotazioni"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(String, ForeignKey("users.id"))
    data = Column(Date)
    flgMattina = Column(Boolean)
    flgPomeriggio = Column(Boolean)
    pin = Column(String)
    wifiAccess = Column(String)
