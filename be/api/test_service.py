from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import auth
from ..service import service_prova

router = APIRouter(
    prefix="/test-service",
    tags=["test-service"]
)

@router.get("/", dependencies=[Depends(auth.RoleChecker(["admin"]))])
def get_service_data(db: Session = Depends(auth.get_db)):
    """
    Test endpoint that calls service_prova logic.
    Restricted to admin for demonstration.
    """
    return service_prova.get_users_with_payments(db)

@router.get("/v2", dependencies=[Depends(auth.RoleChecker(["admin"]))])
def get_service_data_v2(db: Session = Depends(auth.get_db)):
    """
    Test endpoint v2 that calls optimized service_prova logic.
    """
    return service_prova.get_users_with_payments_v2(db)
