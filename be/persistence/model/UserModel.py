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
    cf = Column(String)
    indirizzoResidenza = Column(String)
    citta = Column(String)
    cap = Column(String)
    prov = Column(String)
    regioneSociale = Column(String)
    piva = Column(String)
    telefono = Column(String)
    avatar = Column(String)
    stato = Column(String) # Country/State of residence
    user_status = Column(String, default="ATTIVO") # Account Status: ATTIVO/DISATTIVO

    def __init__(self, **kwargs):
        import random
        super().__init__(**kwargs)
        if not self.avatar:
            self.avatar = random.choice([
                "/src/assets/images/avatars/avatar-1.png",
                "/src/assets/images/avatars/avatar-2.png",
                "/src/assets/images/avatars/avatar-3.png",
                "/src/assets/images/avatars/avatar-4.png",
                "/src/assets/images/avatars/avatar-5.png"
            ])
        if not self.stato:
            self.stato = "ATTIVO"
