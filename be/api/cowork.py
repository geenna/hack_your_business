from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as models
from ..persistence.model.ServiziModel import Servizi
from ..persistence.schemas import UserSchema as user_schema
from ..persistence.schemas import CoWorkSchema as cowork_schema
# Role Based Endpoints
allow_admin_only = auth.RoleChecker(["all"])
allow_user_only = auth.RoleChecker(["user"])


router = APIRouter(
    prefix="/cowork",
    tags=["cowork"]
)

@router.get("/servizi", response_model=List[cowork_schema.ServiziCoWorkSchema])
def getServiziCoWork( db: Session = Depends(auth.get_db), user: models.User = Depends(auth.get_current_user)):
    stmt = select(Servizi)
    results = db.execute(stmt).scalars().all()
    return results

@router.post("/servizi", response_model=cowork_schema.ServiziCoWorkSchema)
def upsertServizioCoWork(
    servizio: cowork_schema.ServiziCoWorkSchema,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)
):
    db_servizio = None
    if servizio.id and servizio.id.strip():
        stmt = select(Servizi).where(Servizi.id == servizio.id)
        db_servizio = db.execute(stmt).scalars().first()

    if db_servizio:
        db_servizio.nome = servizio.nome
        db_servizio.key = servizio.key
        db_servizio.costoIntero = servizio.costoIntero
        db_servizio.costoRidotto = servizio.costoRidotto
    else:
        create_kwargs = {
            "nome": servizio.nome,
            "key": servizio.key,
            "costoIntero": servizio.costoIntero,
            "costoRidotto": servizio.costoRidotto,
        }
        if servizio.id and servizio.id.strip():
            create_kwargs["id"] = servizio.id
        db_servizio = Servizi(**create_kwargs)
        db.add(db_servizio)

    db.commit()
    db.refresh(db_servizio)
    return db_servizio

@router.delete("/servizi/{servizio_id}", status_code=204)
def deleteServizioCoWork(
    servizio_id: str,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)
):
    servizio = db.query(Servizi).filter(Servizi.id == servizio_id).first()
    if not servizio:
        raise HTTPException(status_code=404, detail="Servizio not found")
    db.delete(servizio)
    db.commit()
    return None