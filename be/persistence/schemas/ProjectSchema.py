from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta
from typing import Optional, List
from .UserToProjectSchema import UserToProjectBase
from .UserSchema import UserBase

class ProjectBase(BaseModel):
    projectName: Optional[str] = None
    descrizioneProgetto: Optional[str] = None
    datInizio: Optional[datetime] = None
    datFine: Optional[datetime] = None
    avanzamento: Optional[float] = None
    costo: Optional[float] = None
    stato: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
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
    id: str
    @field_validator('stato')
    @classmethod
    def check_stato(cls, v: str, info) -> str:
        # Inserisci qui la tua logica
        # Esempio: calcola stato basato su date, o trasforma il valore
        # Non lo so, da capire se lo stato deve essere calcolato dinamicamente o se è un campo statico
        avanzamento = info.data.get('avanzamento')
        if avanzamento is not None and avanzamento >= 100:
            return 'COMPLETED'
        elif info.data.get('datFine') and info.data.get('datFine') < datetime.now():
            return 'EXPIRED'
        elif info.data.get('datFine') and info.data.get('datFine') < datetime.now() + timedelta(days=30):
            return 'EXPIRING'
        else:
            return 'IN PROGRESS'
        return v

class ProjectFullResponse(ProjectFull):
    serverTime: datetime
    users: List[UserBase]

class AddCollaboratorRequest(BaseModel):
    userIds: List[str]