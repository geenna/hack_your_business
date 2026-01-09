from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Role(BaseModel):
    action: str
    subject: str

class UserBase(BaseModel):
    email: EmailStr
    userType: str
    roles: List[Role] = []
    nome: Optional[str] = None
    cognome: Optional[str] = None
    cf: Optional[str] = None
    indirizzoResidenza: Optional[str] = None
    citta: Optional[str] = None
    cap: Optional[str] = None
    prov: Optional[str] = None
    regioneSociale: Optional[str] = None
    piva: Optional[str] = None
    telefono: Optional[str] = None
    stato: Optional[str] = None # Country
    user_status: Optional[str] = "ATTIVO" # Account Status
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_ability_rules: List[dict]
    user_data: dict

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str


class UserDetailResponse(UserBase):
    id: str