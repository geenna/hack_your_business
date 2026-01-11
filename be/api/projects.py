from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as models
from ..persistence.model.BillingAddressModel import BillingAddressModel
from ..persistence.schemas import UserSchema as schemas
from ..persistence.schemas import ProjectSchema as project_schemas
from ..service import billing_service
from ..service import project_service

# Role Based Endpoints
allow_admin_only = auth.RoleChecker(["all"])
allow_user_only = auth.RoleChecker(["user"])


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.get("/all-projects/{user_id}", response_model=List[project_schemas.ProjectWithRelation])
def read_users(user_id: str, db: Session = Depends(auth.get_db), user: models.User = Depends(allow_admin_only)):

    results = project_service.get_projects_by_user(user_id, db)
    projects_data = []
    for project, relation in results:
        project_dict = {
            "id": project.id,
            "projectName": project.projectName,
            "descrizioneProgetto": project.descrizioneProgetto,
            "datInizio": project.datInizio,
            "datFine": project.datFine,
            "stato": project.stato,
            "avanzamento": project.avanzamento,
            "role": relation.role,
            "active": relation.active,
            "datCreation": relation.datCreation,
            "costo": project.costo
        }
        projects_data.append(project_dict)
    return projects_data
    
@router.get("/user-projects/", response_model=List[project_schemas.ProjectWithRelation])
def read_users(db: Session = Depends(auth.get_db), user: models.User = Depends(auth.get_current_user)):

    results = project_service.get_projects_by_user(user.id, db)
    projects_data = []
    for project, relation in results:
        project_dict = {
            "id": project.id,
            "projectName": project.projectName,
            "descrizioneProgetto": project.descrizioneProgetto,
            "datInizio": project.datInizio,
            "datFine": project.datFine,
            "stato": project.stato,
            "avanzamento": project.avanzamento,
            "role": relation.role,
            "active": relation.active,
            "datCreation": relation.datCreation
        }
        projects_data.append(project_dict)
    return projects_data