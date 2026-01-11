from ..persistence.model.BillingAddressModel import BillingAddressModel 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from ..persistence.model.UserToProjectModel import UserToProject
from ..persistence.model.ProjectModel import Projects
from typing import List

def get_projects_by_user(user_id: str, db: Session, joinUser = False) -> List[tuple[Projects, UserToProject]]:
    
    #stmt = select(models.User, BillingAddressModel).outerjoin(BillingAddressModel, models.User.id == BillingAddressModel.userId).where(models.User.id == user_id)
    stmt = select(Projects, UserToProject).join(UserToProject).where(UserToProject.userId == user_id)

    if joinUser:
        pass
        #stmt = stmt.join(UserToProject).join(models.User)
    
    result = db.execute(stmt).all()
    return result