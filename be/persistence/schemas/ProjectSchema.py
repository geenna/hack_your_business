from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectBase(BaseModel):
    projectName: Optional[str] = None
    descrizioneProgetto: Optional[str] = None
    datInizio: Optional[datetime] = None
    datFine: Optional[datetime] = None
    stato: Optional[str] = None
    avanzamento: Optional[float] = None
    costo: Optional[float] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: str

    class Config:
        from_attributes = True

class ProjectWithRelation(ProjectResponse):
    role: Optional[str] = None
    active: Optional[bool] = None
    datCreation: Optional[datetime] = None
