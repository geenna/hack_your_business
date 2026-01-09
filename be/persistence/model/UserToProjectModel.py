from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, PrimaryKeyConstraint
from datetime import datetime
from ..database import Base

class UserToProject(Base):
    __tablename__ = "userToProject"

    userId = Column(String, ForeignKey("users.id"))
    projectId = Column(String, ForeignKey("projects.id"))
    role = Column(String)
    datCreation = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    __table_args__ = (
        PrimaryKeyConstraint('userId', 'projectId'),
    )
