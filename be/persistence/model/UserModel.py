from sqlalchemy import Column, String, JSON
import uuid
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    userType = Column(String)
    roles = Column(JSON) # List[dict] stored as JSON: [{action: str, subject: str}]
    nome = Column(String)
    cognome = Column(String)
