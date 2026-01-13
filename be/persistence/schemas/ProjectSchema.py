from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from .UserToProjectSchema import UserToProjectBase
from .UserSchema import UserBase

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


class ProjectFull(ProjectBase):
    userToProjects: Optional[List[UserToProjectBase]] = None
    
    @field_validator('stato')
    @classmethod
    def check_stato(cls, v: str, info) -> str:
        # Inserisci qui la tua logica
        # Esempio: calcola stato basato su date, o trasforma il valore
        # Non lo so, da capire se lo stato deve essere calcolato dinamicamente o se è un campo statico
        if info.data.get('stato') == 'IN_PROGRESS' and info.data.get('avanzamento') < 100:
            if info.data.get('datFine') < datetime.now():
                return 'EXPIRED'
            elif (info.data.get('datFine') - datetime.now()).days < 30:
                return 'EXPIRING'
        return v

class ProjectFullResponse(ProjectFull):
    serverTime: datetime
    users: List[UserBase]