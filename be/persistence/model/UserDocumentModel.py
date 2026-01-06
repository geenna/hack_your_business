from sqlalchemy import Column, String, ForeignKey, DateTime
import uuid
from datetime import datetime
from ..database import Base

class UserDocument(Base):
    __tablename__ = "USER_DOCUMENTS"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    basePath = Column(String)
    fileNameDisk = Column(String)
    fileNameOriginal = Column(String)
    contentType = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)
