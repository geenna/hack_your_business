from sqlalchemy import Column, String, ForeignKey, DateTime
import uuid
from datetime import datetime
from ..database import Base

class ProjectDocument(Base):
    __tablename__ = "PROJ_DOCUMENT"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    projectId = Column(String, ForeignKey("Projects.id", ondelete="CASCADE"))
    basePath = Column(String)
    fileNameDisk = Column(String)
    fileNameOriginal = Column(String)
    contentType = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)
