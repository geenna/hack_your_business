from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectBase(BaseModel):
    descrizioneProgetto: str
    datInizio: Optional[datetime] = None
    datFine: Optional[datetime] = None
    stato: str
    avanzamento: float
    allowedUserId: List[str] = []

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: str
    userId: str

    class Config:
        from_attributes = True
