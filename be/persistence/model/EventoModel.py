from sqlalchemy import Column, String, DateTime, JSON, Boolean
import uuid
from ..database import Base

class Evento(Base):
    __tablename__ = "eventi"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    url = Column(String, nullable=True)
    title = Column(String)
    allDay = Column(Boolean, default=False)
    guests = Column(JSON) # List[str] of user IDs
    calendar = Column(String) # [Collaboratori, Pubblico, Personale]
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
