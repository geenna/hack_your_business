from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import timedelta
from .. import auth
from ..persistence.model import UserModel as models
from ..persistence.schemas import UserSchema as schemas
from ..persistence.database import SessionLocal, engine

router = APIRouter(
    tags=["authentication"]
)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(user_login: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    stmt = select(models.User).where(models.User.email == user_login.username)
    user = db.execute(stmt).scalars().first()
    if not user or not auth.verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_ability_rules": user.roles, 
        "user_data" :{
            "id": user.id,
            "email": user.email,
            "role": user.userType,
            "full_name": user.nome + " " + user.cognome
        },
    }
