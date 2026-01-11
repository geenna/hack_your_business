from sqlalchemy import Column, String, ForeignKey, Float, DateTime, JSON
import uuid
from datetime import datetime
from ..database import Base

class Projects(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    projectName = Column(String)
    descrizioneProgetto = Column(String)
    datInizio = Column(DateTime, default=datetime.utcnow)
    datFine = Column(DateTime)
    stato = Column(String)
    avanzamento = Column(Float)
    costo = Column(Float)