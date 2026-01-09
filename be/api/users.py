from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as models
from ..persistence.schemas import UserSchema as schemas


# Role Based Endpoints
allow_admin_only = auth.RoleChecker(["all"])
allow_user_only = auth.RoleChecker(["user"])



router = APIRouter(
    tags=["users"]
)

@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(allow_admin_only)):
    stmt = select(models.User).where(models.User.email == user.email)
    db_user = db.execute(stmt).scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        userType=user.userType.lower(),
        roles=[{"action": "all", "subject": user.userType.lower()}],
        nome=user.nome,
        cognome=user.cognome,
        cf=user.cf,
        indirizzoResidenza=user.indirizzoResidenza,
        citta=user.citta,
        cap=user.cap,
        prov=user.prov,
        regioneSociale=user.regioneSociale,
        piva=user.piva,
        telefono=user.telefono,
        stato=user.stato,
        user_status=user.user_status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(allow_admin_only)):
    stmt = select(models.User).where(models.User.id == user_id)
    db_user = db.execute(stmt).scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        if key == 'password' and value:
             setattr(db_user, 'hashed_password', auth.get_password_hash(value))
        elif key != 'password':
             setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}/suspend", response_model=schemas.UserResponse)
def suspend_user(user_id: str, db: Session = Depends(auth.get_db), current_user: models.User = Depends(allow_admin_only)):
    stmt = select(models.User).where(models.User.id == user_id)
    db_user = db.execute(stmt).scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.user_status = "DISATTIVO"
    db.commit()
    db.refresh(db_user)
    return db_user
    
@router.put("/users/{user_id}/activate", response_model=schemas.UserResponse)
def activate_user(user_id: str, db: Session = Depends(auth.get_db), current_user: models.User = Depends(allow_admin_only)):
    stmt = select(models.User).where(models.User.id == user_id)
    db_user = db.execute(stmt).scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.user_status = "ATTIVO"
    db.commit()
    db.refresh(db_user)
    return db_user



@router.get("/users", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(auth.get_db), user: models.User = Depends(allow_admin_only)):
    stmt = select(models.User)
    users = db.execute(stmt).scalars().all()
    return users
    

@router.get("/user-detail/{user_id}", response_model=schemas.UserDetailResponse)
def read_user_detail(user_id: str, db: Session = Depends(auth.get_db), current_user: models.User = Depends(allow_admin_only)):
    stmt = select(models.User).where(models.User.id == user_id)
    user = db.execute(stmt).scalars().first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/admin-data")
def read_admin_data(user: models.User = Depends(allow_admin_only)):
    return {"message": f"Hello {user.email}! You have access to this data."}

@router.get("/user-data")
def read_user_data(user: models.User = Depends(allow_user_only)):
    return {"message": f"Hello {user.email}! You have access to this data."}


@router.get("/all-data")
def read_all_data(user: models.User = Depends(auth.RoleChecker(["user", "admin"]))):
    return {"message": f"Hello {user.email}! You have access to this data."}