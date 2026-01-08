from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from .persistence.database import SessionLocal
from .persistence.model import UserModel as models
from .persistence.schemas import UserSchema as schemas

# CONSTANTS - CHANGE FOR PRODUCTION
SECRET_KEY = "supersecretkeydevelopmentonly"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    stmt = select(models.User).where(models.User.email == token_data.email)
    user = db.execute(stmt).scalars().first()
    if user is None:
        raise credentials_exception
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: models.User = Depends(get_current_user)):
        # Check if user has ANY of the allowed roles
        # Assuming user.roles is a list of strings
        # Check if user has ANY of the allowed roles
        # user.roles is a list of dicts (from JSON column)
        # Adapt string check to look into the 'action' field or 'subject'
        # For now, we assume allowed_roles (strings) map to 'action'
        has_permission = False
        if user.roles:
            for role in user.roles:
                # Handle dict (DB) or object (Pydantic)
                r_action = role.get("subject") if isinstance(role, dict) else getattr(role, "subject", None)
                if r_action in self.allowed_roles:
                    has_permission = True
                    break
        

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Operation not permitted"
            )
        return user
