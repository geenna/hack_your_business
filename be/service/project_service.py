from ..persistence.model.BillingAddressModel import BillingAddressModel 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from ..persistence.model.UserToProjectModel import UserToProject
from ..persistence.model.ProjectModel import Projects
from typing import List

def get_projects_by_user(user_id: str, db: Session) -> List[Projects]:
    
    #stmt = select(models.User, BillingAddressModel).outerjoin(BillingAddressModel, models.User.id == BillingAddressModel.userId).where(models.User.id == user_id)
    stmt = select(Projects).join(UserToProject).filter(UserToProject.userId == user_id)
    result = db.execute(stmt).scalars().all()
    return result