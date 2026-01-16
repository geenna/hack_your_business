from ..persistence.model.BillingAddressModel import BillingAddressModel 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from ..persistence.model.UserToProjectModel import UserToProject
from ..persistence.model.ProjectModel import Projects
from ..persistence.model.UserModel import User
from typing import List

def get_projects_by_user(user_id: str, db: Session, joinUser = False) -> List[tuple[Projects, UserToProject]]:
    
    #stmt = select(models.User, BillingAddressModel).outerjoin(BillingAddressModel, models.User.id == BillingAddressModel.userId).where(models.User.id == user_id)
    stmt = select(Projects, UserToProject).join(UserToProject).where(UserToProject.userId == user_id)

    if joinUser:
        pass
        #stmt = stmt.join(UserToProject).join(models.User)
    
    
    result = db.execute(stmt).all()
    return result

def get_projects_full(db: Session, user_id: str = None) -> List[tuple[Projects, UserToProject, User]]:
    stmt = select(Projects, UserToProject, User)\
        .outerjoin(UserToProject, Projects.id == UserToProject.projectId)\
        .outerjoin(User, UserToProject.userId == User.id)
    
    if user_id:
        stmt = stmt.where(UserToProject.userId == user_id)
        
    result = db.execute(stmt).all()
    return result

def add_collaborators(project_id: str, user_ids: List[str], db: Session):
    for user_id in user_ids:
        # Check if relation already exists
        stmt = select(UserToProject).where(UserToProject.projectId == project_id).where(UserToProject.userId == user_id)
        existing = db.execute(stmt).scalars().first()
        
        if not existing:
            new_relation = UserToProject(
                userId=user_id,
                projectId=project_id,
                role="PROJMANAGER", # Default role
                active=True
            )
            db.add(new_relation)
    
    db.commit()
    return True

def remove_collaborator(project_id: str, user_id: str, db: Session):
    stmt = select(UserToProject).where(UserToProject.projectId == project_id).where(UserToProject.userId == user_id)
    relation = db.execute(stmt).scalars().first()
    
    if relation:
        db.delete(relation)
        db.commit()
        return True
    return False

def update_project(project_id: str, project_data: dict, db: Session):
    stmt = select(Projects).where(Projects.id == project_id)
    project = db.execute(stmt).scalars().first()
    
    if project:
        for key, value in project_data.items():
            if value is not None:
                setattr(project, key, value)
        db.commit()
        db.refresh(project)
        return project
    return None

def delete_project(project_id: str, db: Session):
    # First delete all relations
    stmt = select(UserToProject).where(UserToProject.projectId == project_id)
    relations = db.execute(stmt).scalars().all()
    for relation in relations:
        db.delete(relation)
    
    # Then delete the project
    stmt = select(Projects).where(Projects.id == project_id)
    project = db.execute(stmt).scalars().first()
    
    if project:
        db.delete(project)
        db.commit()
        return True
    
    # If project not found but relations deleted (shouldn't happen with FK normally but safe to have)
    db.commit()
    return False

def create_project(project_data: dict, user_id: str, db: Session):
    try:
        new_project = Projects(**project_data)
        db.add(new_project)
        db.flush() # flush to get id
        
        # Add creator as ADMIN or PROJMANAGER
        new_relation = UserToProject(
            userId=user_id,
            projectId=new_project.id,
            role="PROJMANAGER",
            active=True
        )
        db.add(new_relation)
        
        db.commit()
        db.refresh(new_project)
        return new_project
    except Exception as e:
        db.rollback()
        raise e