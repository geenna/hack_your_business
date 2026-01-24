from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional, Union


class Role(BaseModel):
    action: str
    subject: str


def _roles_to_privilegi(roles: Optional[List[Union[Role, dict]]]) -> List[str]:
    if not roles:
        return []
    privilegi: List[str] = []
    for role in roles:
        if isinstance(role, dict):
            subject = role.get("subject")
        else:
            subject = getattr(role, "subject", None)
        if subject:
            privilegi.append(subject)
    return privilegi


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


class UserWithPrivilegi(UserBase):
    privilegi: List[str] = []

    @field_validator("privilegi", mode="before")
    @classmethod
    def compute_privilegi(cls, v, info):
        if v is not None and v != []:
            return v
        return _roles_to_privilegi(info.data.get("roles"))
    

class UserCreate(UserBase):
    password: str
    privilegi: Optional[List[str]] = []
class UserPasswordChange(BaseModel):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    privilegi: Optional[List[str]] = []
class UserResponse(UserWithPrivilegi):
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
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com",
                "password": "your_password"
            }
        }


from .BillingAddressSchema import BillingAddressSchema

class UserDetailResponse(UserWithPrivilegi):
    id: str
    billing_address: Optional[BillingAddressSchema] = None
