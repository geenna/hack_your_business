from sqlalchemy import Column, String, Float
import uuid
from ..database import Base


class Servizi(Base):
    __tablename__ = "servizi"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String)
    key = Column(String)
    costoIntero = Column(Float)
    costoRidotto = Column(Float)
