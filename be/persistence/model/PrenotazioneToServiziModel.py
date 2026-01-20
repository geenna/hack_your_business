from sqlalchemy import Column, String, ForeignKey
import uuid
from ..database import Base


class PrenotazioneToServizi(Base):
    __tablename__ = "prenotazioneToServizi"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    idPrenotazione = Column(String, ForeignKey("prenotazioni.id"))
    idServizio = Column(String, ForeignKey("servizi.id"))
