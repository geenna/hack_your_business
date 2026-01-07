from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    userType: str

class Role(BaseModel):
    action: str
    subject: str

class UserBase(BaseModel):
    email: EmailStr
    userType: str
    roles: List[Role] = []
    nome: str
    cognome: str

class UserCreate(UserBase):
    password: str

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
