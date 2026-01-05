from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as models
from ..persistence.schemas import UserSchema as schemas

router = APIRouter(
    tags=["users"]
)

@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    stmt = select(models.User).where(models.User.email == user.email)
    db_user = db.execute(stmt).scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        userType=user.userType,
        roles=user.roles,
        nome=user.nome,
        cognome=user.cognome
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Role Based Endpoints
allow_admin_only = auth.RoleChecker(["admin"])
allow_user_only = auth.RoleChecker(["user"])

@router.get("/admin-data")
def read_admin_data(user: models.User = Depends(allow_admin_only)):
    return {"message": f"Hello {user.email}! You have access to this data."}

@router.get("/user-data")
def read_user_data(user: models.User = Depends(allow_user_only)):
    return {"message": f"Hello {user.email}! You have access to this data."}


@router.get("/all-data")
def read_all_data(user: models.User = Depends(auth.RoleChecker(["user", "admin"]))):
    return {"message": f"Hello {user.email}! You have access to this data."}