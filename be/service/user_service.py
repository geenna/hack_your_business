from sqlalchemy.orm import Session
from sqlalchemy import select
from ..persistence.model import UserModel as models
from typing import List

def get_users_by_ids(db: Session, user_ids: List[str]) -> List[models.User]:
    """
    Fetch users by a list of IDs.
    """
    if not user_ids:
        return []
    
    stmt = select(models.User).where(models.User.id.in_(user_ids))
    users = db.execute(stmt).scalars().all()
    return users
