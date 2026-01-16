from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .UserSchema import UserBase

class UserToProjectBase(BaseModel):
    userId: Optional[str] = None
    projectId: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None
    datCreation: Optional[datetime] = None
    avanzamento: Optional[int] = None

class UserToProjectCreate(UserToProjectBase):
    pass

class UserToProjectResponse(UserToProjectBase):
    id: str

    class Config:
        from_attributes = True

class UserToProjectFull(UserToProjectBase):
    users: Optional[List[UserBase]] = None